"""Command line: ``irvalidate <kind> <value>`` or ``irvalidate <kind> --generate``."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable

from . import (
    ValidationResult,
    card_bank,
    generate_card_number,
    generate_landline,
    generate_legal_id,
    generate_mobile,
    generate_national_id,
    generate_postal_code,
    generate_sheba,
    landline_area,
    mobile_operator,
    sheba_bank,
    validate_card_number,
    validate_landline,
    validate_legal_id,
    validate_mobile,
    validate_national_id,
    validate_postal_code,
    validate_sheba,
)

_VALIDATE: dict[str, Callable[[object], ValidationResult]] = {
    "national-id": validate_national_id,
    "legal-id": validate_legal_id,
    "card": validate_card_number,
    "sheba": validate_sheba,
    "mobile": validate_mobile,
    "landline": validate_landline,
    "postal-code": validate_postal_code,
}

_GENERATE: dict[str, Callable[[], str]] = {
    "national-id": generate_national_id,
    "legal-id": generate_legal_id,
    "card": generate_card_number,
    "sheba": generate_sheba,
    "mobile": generate_mobile,
    "landline": generate_landline,
    "postal-code": generate_postal_code,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="irvalidate", description="Validate (or generate test) Iranian data."
    )
    parser.add_argument("kind", choices=sorted(_VALIDATE))
    parser.add_argument("value", nargs="?", help="the value to validate")
    parser.add_argument(
        "--generate", action="store_true", help="print a valid random test value instead"
    )
    args = parser.parse_args(argv)

    if args.generate:
        print(_GENERATE[args.kind]())
        return 0
    if args.value is None:
        parser.error("a value is required unless --generate is used")

    result = _VALIDATE[args.kind](args.value)
    if not result.ok:
        print("invalid")
        print(f"reason: {result.code} ({result.message_en})")
        return 1

    print("valid")
    extra = None
    if args.kind == "card":
        extra = card_bank(args.value)
    elif args.kind == "sheba":
        extra = sheba_bank(args.value)
    if extra:
        print(f"bank: {extra.name_fa} ({extra.name_en})")
    if args.kind == "mobile":
        op = mobile_operator(args.value)
        if op:
            print(f"operator: {op}")
    if args.kind == "landline":
        area = landline_area(args.value)
        if area:
            print(f"province: {area.province_fa} ({area.province_en})")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
