#!/usr/bin/env python3

import argparse
import csv
import os
import random
import re
import sys
from datetime import date, timedelta
from getpass import getpass

from dateutil import parser as dateparser
import psycopg2
from psycopg2 import sql


def clean_customer_id(raw):
    if raw is None:
        return None

    cid = str(raw).strip()

    if cid == "":
        return None

    cid = re.sub(r"\s+", "", cid)

    return cid.upper()

def extract_ids_from_csv(csv_path):
    ids = []

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        headers = [h.strip() for h in reader.fieldnames] if reader.fieldnames else []
        id_key = None

        for cand in headers:
            low = cand.lower().strip()

            if low in {"customer_id", "customerid", "cust_id"}:
                id_key = cand
                break

        if id_key is None:
            for cand in headers:
                if cand.lower().strip() == "id":
                    id_key = cand
                    break

        if id_key is None:
            raise ValueError("Could not find a customer id column in the CSV. Expected 'customer_id' or similar.")

        for row in reader:
            cid = clean_customer_id(row.get(id_key))

            if cid:
                ids.append(cid)

    unique = sorted(set(ids))

    return unique

FIRST_NAMES_MALE = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles', 'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua', 'Kevin', 'Brian', 'George', 'Timothy', 'Ronald', 'Edward', 'Jason', 'Jeffrey', 'Ryan', 'Jacob', 'Gary', 'Nicholas', 'Eric', 'Stephen', 'Jonathan', 'Larry', 'Justin', 'Scott', 'Brandon', 'Benjamin', 'Samuel', 'Gregory', 'Alexander', 'Frank', 'Patrick', 'Raymond', 'Jack', 'Dennis', 'Jerry', 'Tyler']
FIRST_NAMES_FEMALE = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen', 'Nancy', 'Lisa', 'Betty', 'Margaret', 'Sandra', 'Ashley', 'Kimberly', 'Emily', 'Donna', 'Michelle', 'Carol', 'Amanda', 'Dorothy', 'Melissa', 'Deborah', 'Stephanie', 'Rebecca', 'Sharon', 'Laura', 'Cynthia', 'Amy', 'Kathleen', 'Angela', 'Shirley', 'Anna', 'Brenda', 'Pamela', 'Emma', 'Nicole', 'Samantha', 'Katherine', 'Christine', 'Debra', 'Rachel', 'Catherine', 'Carolyn', 'Janet', 'Heather', 'Diane', 'Julie']
LAST_NAMES = LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Miller","Davis","Garcia","Rodriguez","Martinez", "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin", "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson", "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores"]
GENDERS = ["female", "male"]
JOBS = ["Data Analyst","Product Manager","Software Engineer","Sales Associate","UX Designer","Accountant", "Marketing Specialist","Operations Manager","Customer Support","Business Analyst","Consultant", "Financial Analyst","HR Generalist","Project Manager","QA Tester","DevOps Engineer","Data Scientist", "Content Strategist","Graphic Designer","Researcher","Teacher","Nurse","Chef","Barista","Librarian"]


def make_birth_date(rng):
    start = date(1958, 1, 1)
    end = date(2004, 12, 31)
    days = (end - start).days

    return start + timedelta(days=rng.randint(0, days))

def synthesize_profile(customer_id, rng):
    gender = rng.choice(GENDERS)  # 'female' or 'male'

    if gender == "male":
        first = rng.choice(FIRST_NAMES_MALE)
    else:
        first = rng.choice(FIRST_NAMES_FEMALE)

    last = rng.choice(LAST_NAMES)
    job = rng.choice(JOBS)
    dob = make_birth_date(rng)

    return {
        "customer_id": customer_id,
        "first_name": first,
        "last_name": last,
        "gender": gender,
        "job_title": job,
        "birth_date": dob.isoformat(),
    }

def generate_new_ids(existing_ids, count_extra):
    if not existing_ids:
        return [f"C{str(i).zfill(4)}" for i in range(1, count_extra + 1)]

    nums = []
    for cid in existing_ids:
        m = re.match(r"^[A-Za-z]*?(\d+)$", cid)

        if m:
            nums.append(int(m.group(1)))

    base_letter = "C"

    if nums:
        start = max(nums) + 1
        width = max(len(str(n)) for n in nums)
        out = []
        i = start

        while len(out) < count_extra:
            cid = f"{base_letter}{str(i).zfill(width)}"

            if cid not in existing_ids:
                out.append(cid)

            i += 1

        return out

    out = []
    i = 1
    existing_set = set(existing_ids)

    while len(out) < count_extra:
        cid = f"NEW{i:05d}"

        if cid not in existing_set:
            out.append(cid)

        i += 1

    return out


DDL = """
CREATE TABLE IF NOT EXISTS {table_ident} (
    customer_id    TEXT PRIMARY KEY,
    first_name     TEXT NOT NULL,
    last_name      TEXT NOT NULL,
    gender         TEXT CHECK (gender IN ('female','male')) NOT NULL,
    job_title      TEXT NOT NULL,
    birth_date     DATE NOT NULL,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

UPSERT = """
INSERT INTO {table_ident} (customer_id, first_name, last_name, gender, job_title, birth_date)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (customer_id) DO UPDATE
SET first_name = EXCLUDED.first_name,
    last_name  = EXCLUDED.last_name,
    gender     = EXCLUDED.gender,
    job_title  = EXCLUDED.job_title,
    birth_date = EXCLUDED.birth_date;
"""

def create_database_if_needed(conn_params, dbname):
    from psycopg2 import extensions

    tmp = conn_params.copy()
    tmp["dbname"] = "postgres"
    conn = psycopg2.connect(**tmp)

    try:
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
            exists = cur.fetchone() is not None

            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
                print(f"Created database: {dbname}")
            else:
                print(f"Database already exists: {dbname}")
    finally:
        conn.close()

def ensure_table(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(sql.SQL(DDL).format(table_ident=sql.Identifier(table_name)))
    conn.commit()

def upsert_profiles(conn, table_name, profiles):
    with conn.cursor() as cur:
        args = [(p["customer_id"], p["first_name"], p["last_name"], p["gender"], p["job_title"], p["birth_date"]) for p in profiles]
        psycopg2.extras.execute_batch(
            cur,
            sql.SQL(UPSERT).format(table_ident=sql.Identifier(table_name)).as_string(conn),
            args,
            page_size=1000
        )
    conn.commit()

def main():
    parser = argparse.ArgumentParser(description="Create and load a PostgreSQL table of customer profiles.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5432)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", help="If omitted, you will be prompted.")
    parser.add_argument("--database", required=True, help="Target database name.")
    parser.add_argument("--create-db", action="store_true", help="Create the database if it doesn't exist.")
    parser.add_argument("--csv", required=True, help="Path to the messy CSV containing customer IDs.")
    parser.add_argument("--table", default="customers", help="Target table name to create/fill.")
    parser.add_argument("--extras", type=int, default=50, help="How many additional synthetic customer_ids to add beyond the CSV.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility.")
    args = parser.parse_args()

    pwd = args.password or getpass("PostgreSQL password: ")

    csv_ids = extract_ids_from_csv(args.csv)
    print(f"Found {len(csv_ids)} unique customer_ids in CSV.")

    extra_ids = generate_new_ids(csv_ids, args.extras) if args.extras > 0 else []
    print(f"Generated {len(extra_ids)} extra customer_ids.")

    all_ids = csv_ids + extra_ids

    base_conn_params = {
        "host": args.host,
        "port": args.port,
        "user": args.user,
        "password": pwd,
    }

    if args.create_db:
        create_database_if_needed(base_conn_params, args.database)

    conn_params = base_conn_params.copy()
    conn_params["dbname"] = args.database

    with psycopg2.connect(**conn_params) as conn:
        ensure_table(conn, args.table)

        rng = random.Random(args.seed)
        profiles = [synthesize_profile(cid, rng) for cid in all_ids]

        from psycopg2 import extras
        globals()["psycopg2"].extras = extras
        upsert_profiles(conn, args.table, profiles)

        with conn.cursor() as cur:
            cur.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(args.table)))
            total = cur.fetchone()[0]
            cur.execute(sql.SQL("SELECT COUNT(*) FROM {} WHERE customer_id = ANY(%s)").format(sql.Identifier(args.table)), (all_ids,))
            present = cur.fetchone()[0]

        print(f"Upserted {len(all_ids)} profiles.")
        print(f"Table row count now: {total}. CSV+extra present: {present}.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
