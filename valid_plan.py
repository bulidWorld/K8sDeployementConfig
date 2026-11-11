#!/usr/bin/env python3
"""Validate a deployment execution plan against deployment-plan.xsd."""

from __future__ import annotations

import argparse
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an execution plan XML file against its XSD schema."
    )
    parser.add_argument(
        "xml",
        nargs="?",
        type=Path,
        default=Path("PrometheusDeployement/execution-plan.xml"),
        help="execution plan to validate (default: PrometheusDeployement/execution-plan.xml)",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=ROOT / "deployment-plan.xsd",
        help="XSD schema (default: deployment-plan.xsd next to this script)",
    )
    args = parser.parse_args()

    xml_path = args.xml.resolve()
    schema_path = args.schema.resolve()

    try:
        schema_doc = etree.parse(str(schema_path))
        schema = etree.XMLSchema(schema_doc)
        xml_doc = etree.parse(str(xml_path))
    except (OSError, etree.XMLSyntaxError, etree.XMLSchemaParseError) as exc:
        print("False")
        return 2

    is_valid = schema.validate(xml_doc)
    print("True" if is_valid else "False")
    return 0 if is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
