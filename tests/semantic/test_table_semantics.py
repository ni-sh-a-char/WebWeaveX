from core.semantic.table_semantics_engine import extract_table_semantics


def test_table_invoice_detection():
    html = """
    <table><tr><th>Invoice</th><th>Amount Due</th></tr>
    <tr><td>1001</td><td>50</td></tr></table>
    """

    tables = extract_table_semantics(html)

    assert tables["tables"][0]["kinds"][0] == "invoice"
