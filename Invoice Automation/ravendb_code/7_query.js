from "Invoices"
where vector.search(embedding.text(text, ai.task("embed")), "I bought some keyboard stuff", 0.7)
