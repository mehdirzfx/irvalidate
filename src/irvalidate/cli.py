"""Command line: ``irvalidate <kind> <value>``."""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import (
    card_bank,
    is_valid_card_number,
    is_valid_legal_id,
    is_valid_mobile,
    is_valid_national_id,
    is_valid_postal_code,
    is_valid_sheba,
    mobile_operator,
    sheba_bank,
)

_CHECKS = {
    "national-id": is_valid_national_id,
    "legal-id": is_valid_legal_id,
    "card": is_valid_card_number,
    "sheba": is_valid_sheba,
    "mobile": is_valid_mobile,
    "postal-code": is_valid_postal_code,
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="irvalidate", description="Validate Iranian data.")
    parser.add_argument("kind", choices=sorted(_CHECKS))
    parser.add_argument("value")
    args = parser.parse_args(argv)

    ok = _CHECKS[args.kind](args.value)
    print("valid" if ok else "invalid")
    if ok:
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
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
