from core.repository.terraform_semantic_engine import (
    parse_terraform_semantics,
)


def test_tf_parse():

    text = '''
resource "aws_s3_bucket" "b" {}
'''

    r = parse_terraform_semantics(text)

    assert r["count"] == 1
