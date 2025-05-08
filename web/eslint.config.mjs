import { dirname } from "path";
import { fileURLToPath } from "url";

import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
    baseDirectory: __dirname,
});

const eslintConfig = [
    ...compat.plugins("@typescript-eslint", "prettier", "import"),
    ...compat.extends(
        "plugin:@typescript-eslint/recommended",
        "plugin:prettier/recommended",
        "next/core-web-vitals",
        "next/typescript",
        "plugin:import/recommended",
        "plugin:import/typescript",
    ),
    {
        rules: {
            "sort-imports": [
                "warn",
                {
                    ignoreCase: false,
                    ignoreDeclarationSort: true,
                    ignoreMemberSort: false,
                    memberSyntaxSortOrder: ["none", "all", "multiple", "single"],
                    allowSeparatedGroups: true,
                },
            ],
            "import/order": [
                "warn",
                {
                    groups: ["builtin", "external", "internal", ["sibling", "parent"], "index", "unknown"],
                    "newlines-between": "always",
                    alphabetize: {
                        order: "asc",
                        caseInsensitive: true,
                    },
                },
            ],
            "@typescript-eslint/no-empty-object-type": [
                "error",
                {
                    allowObjectTypes: "always",
                },
            ],
            "@typescript-eslint/no-explicit-any": "off",
            "@typescript-eslint/no-unused-vars": "off",
        },
    },
];

export default eslintConfig;
