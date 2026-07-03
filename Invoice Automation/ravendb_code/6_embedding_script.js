embeddings.generate({
    text: `Seller: ${this.seller_party_name}
Buyer: ${this.buyer_party_name}
Total: ${this.invoice_total}
Items: ${(this.invoice_positions || []).map(p => `${p.item} x${p.quantity}`)}
`;
});
