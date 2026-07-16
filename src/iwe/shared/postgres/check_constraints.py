from typing import Final

from sqlalchemy import CheckConstraint, text


CHK_DISHES_ROOT_STRUCTURE_AND_TYPES: Final[CheckConstraint] = CheckConstraint(
    text(
        "(info -> 'name') IS NOT NULL AND (jsonb_typeof(info -> 'name') = 'string') AND "
        "(info -> 'meta') IS NOT NULL AND (jsonb_typeof(info -> 'meta') = 'object') AND "
        "(info -> 'origin_and_recipe') IS NOT NULL AND (jsonb_typeof(info -> 'origin_and_recipe') = 'object')"
    ),
    name="chk_dishes_root_structure_and_types",
)

CHK_DISHES_NAME_RULES: Final[CheckConstraint] = CheckConstraint(
    text("(length(info ->> 'name') BETWEEN 5 AND 67) AND (info ->> 'name' ~* 'burger')"),
    name="chk_dishes_name_rules",
)

CHK_DISHES_STATIC_META_METRICS: Final[CheckConstraint] = CheckConstraint(
    text("""
        (jsonb_typeof(info -> 'meta' -> 'weight_g') = 'number' AND (info -> 'meta' -> 'weight_g')::text::float > 0) AND
        (jsonb_typeof(info -> 'meta' -> 'is_vegan') = 'boolean') AND
        (jsonb_typeof(info -> 'meta' -> 'is_psyop') = 'boolean') AND

        (jsonb_typeof(info -> 'meta' -> 'macro' -> 'calories') = 'number' AND (info -> 'meta' -> 'macro' ->> 'calories')::float >= 0) AND
        (jsonb_typeof(info -> 'meta' -> 'macro' -> 'proteins_g') = 'number' AND (info -> 'meta' -> 'macro' ->> 'proteins_g')::float >= 0) AND
        (jsonb_typeof(info -> 'meta' -> 'macro' -> 'fats_g') = 'number' AND (info -> 'meta' -> 'macro' ->> 'fats_g')::float >= 0) AND
        (jsonb_typeof(info -> 'meta' -> 'macro' -> 'carbs_g') = 'number' AND (info -> 'meta' -> 'macro' ->> 'carbs_g')::float >= 0) AND

        (jsonb_typeof(info -> 'meta' -> 'micro_and_toxic' -> 'saturated_fats_g') = 'number' AND (info -> 'meta' -> 'micro_and_toxic' ->> 'saturated_fats_g')::float >= 0) AND
        (jsonb_typeof(info -> 'meta' -> 'micro_and_toxic' -> 'trans_fats_g') = 'number' AND (info -> 'meta' -> 'micro_and_toxic' ->> 'trans_fats_g')::float >= 0) AND
        (jsonb_typeof(info -> 'meta' -> 'micro_and_toxic' -> 'lead_g') = 'number' AND (info -> 'meta' -> 'micro_and_toxic' ->> 'lead_g')::float >= 0) AND
        (jsonb_typeof(info -> 'meta' -> 'micro_and_toxic' -> 'rat_poison_g') = 'number' AND (info -> 'meta' -> 'micro_and_toxic' ->> 'rat_poison_g')::float >= 0) AND

        (jsonb_typeof(info -> 'meta' -> 'macro' -> 'water_percentage') = 'number' AND
        (info -> 'meta' -> 'macro' ->> 'water_percentage')::float BETWEEN 0.0 AND 100.0)
    """),
    name="chk_dishes_static_meta_metrics",
)

CHK_DISHES_RECIPE_AND_SUPPLY_CHAIN_RULES: Final[CheckConstraint] = CheckConstraint(
    text("""
        (length(info -> 'origin_and_recipe' ->> 'origin_zone') BETWEEN 10 AND 67) AND
        (length(info -> 'origin_and_recipe' ->> 'cooking_process') BETWEEN 10 AND 1488) AND
        (jsonb_typeof(info -> 'origin_and_recipe' -> 'supply_chain') = 'array') AND

        NOT jsonb_path_exists(
            info -> 'origin_and_recipe' -> 'supply_chain',
            '$[*] ? (
                @.merchant_name.type() != "string" ||
                @.location.type() != "string" ||
                @.trust_level.type() != "number" ||
                !(@.merchant_name like_regex "^.{1,67}$") ||
                !(@.location like_regex "^.{1,67}$") ||
                @.trust_level < 0 ||
                @.trust_level > 32767
            )'
        )
    """),
    name="chk_dishes_recipe_and_supply_chain_rules",
)

CHK_DISHES_DYNAMIC_INGREDIENTS_WEIGHT_VALID: Final[CheckConstraint] = CheckConstraint(
    text("""
        (info -> 'origin_and_recipe' -> 'ingredients_weight_g') IS NOT NULL AND
        (jsonb_typeof(info -> 'origin_and_recipe' -> 'ingredients_weight_g') = 'object') AND

        NOT jsonb_path_exists(
            info -> 'origin_and_recipe' -> 'ingredients_weight_g',
            '$.* ? (@.type() != "number" || @ < 0)'
        )
    """),
    name="chk_dishes_dynamic_ingredients_weight_valid",
)
