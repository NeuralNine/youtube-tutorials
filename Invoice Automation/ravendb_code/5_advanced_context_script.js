const attachments = this['@metadata']['@attachments'] || [];

if (attachments.length > 0) {
    const att = attachments[0];
    const file = loadAttachment(att.Name);

    if (file != null) {
        const ctx = ai.genContext({ docId: id(this) });
        const t = att.ContentType;

        if (t == 'application/pdf') ctx.withPdf(file);
        else if (t == 'image/png') ctx.withPng(file);
        else if (t == 'image/jpeg') ctx.withJpeg(file);
        else if (t == 'image/webp') ctx.withWebp(file);
        else if (t == 'image/gif') ctx.withGif(file);
        else if (t == 'text/plain') ctx.withText(file);
    }
}
