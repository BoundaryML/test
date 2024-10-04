###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401
# flake8: noqa: E501,F401
# pylint: disable=unused-import,line-too-long
# fmt: off

file_map = {
    
    "classes/statement_page.baml": "// class Page {\n//     page_number int @alias(\"id\")\n//     contains_transactions bool @alias(\"has_any_transaction_listed\") @description(#\"\n//         Determines whether the bank statement page contains a list of transactions, can have one or more transactions.\n//         Each transaction row is identified by date, description and amount.\n//         Summary should be excluded.\n//         Does not include checks or images of checks.\n//     \"#)\n//     contains_account_summary bool @description(\"Determines whether the page contains account details information (business name, address, account number), not the name and address of a bank.\")\n\n// }\n\nclass PageHasTransactions {\n    page_number int @alias(\"id\")\n    has_transactions bool @alias(\"has_any_transaction_listed\") @description(#\"\n        Determines whether the bank statement page contains a list of transactions, can have one or more transactions.\n        Each transaction row is identified by date, description and amount.\n        Summary should be excluded.\n        Does not include checks or images of checks.\n    \"#)\n}\n\nfunction CheckPageHasTransactions(statement_page: image) -> PageHasTransactions {\n    client Sonnet\n    prompt #\"\n        {{ _.role(\"user\") }}\n        Check whether the provided bank statement page contains a list of transactions.\n        {{ statement_page }}\n        {{ ctx.output_format }}\n    \"#\n}",
    "classes/statement_summary.baml": "\nclass FinancialSummary {\n  bank_name string\n  business_name string\n  business_account_number string\n  business_address string\n  beginning_balance float @alias(\"beginning_balance_gaap_format\")\n  ending_balances EndingBalanceItem[] @alias(\"ending_balances_per_day\")\n  // deposits DepositsItem[] @alias(\"deposits_and_additions\")\n  // withdrawals WithdrawalsItem[]\n  // fees FeesItem[]\n}\n\nclass EndingBalanceItem {\n  date string @alias(\"date_of_ending_balance\")\n  amount float @alias(\"ending_balance_amount\")\n}\n \nfunction ExtractFinancialSummaryData(statements: image[] | string[]) -> FinancialSummary {\n  client Sonnet\n  prompt #\"\n    {# start a user message #}\n    {{ _.role(\"user\") }}\n\n    Scan and extract the financial data from all pages of this bank statement.\n    {{ statements }}\n\n    {# special macro to print the output schema instructions. #}\n    {{ ctx.output_format }}\n  \"#\n}\n",
    "classes/statement_transaction.baml": "class Transaction {\n  date string @alias(\"transaction_date\")\n  description string | null @alias(\"transaction_description\")\n  amount float @alias(\"transaction_amount\")\n  transaction_type TransactionType\n}\n\nenum TransactionType {\n  Deposit @description(\"Deposit or addition\")\n  Withdrawal @description(\"Withdrawal or deduction\")\n  Other @description(\"Other type of transaction like a fee, charge, etc.\")\n}\n\nfunction ExtractStatementPageTransactions(statement_page: image) -> Transaction[] {\n  client Sonnet\n  prompt #\"\n    {{ _.role(\"user\") }}\n    Scan and extract all the transaction items from the provided bank statement page.\n    Each transaction row is identified by date, description and amount.\n    Do not mix transactions with other types of information like summaries or checks.\n    Try not to miss any.\n    {{ statement_page }}\n    {{ ctx.output_format }}\n  \"#\n}\n \nfunction Hi(input: string) -> string {\n  client Sonnet\n  prompt #\"\n    TCouun\n    {{ _.role(\"user\") }}\n    Hi {{ input}} \n\n  \"#\n}\n",
    "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> GPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n  \nclient<llm> Sonnet {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20240620\"\n    api_key env.ANTHROPIC_API_KEY\n    temperature 0\n  }\n}\n\nclient<llm> Claude {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20240620\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\nclient<llm> FastAnthropic {\n  provider anthropic\n  options {\n    model \"claude-3-haiku-20240307\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\nclient<llm> FastOpenAI {\n  provider openai\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> Fast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    // Learn more at https://docs.boundaryml.com/docs/snippets/clients/round-robin\n    strategy [FastAnthropic, FastOpenAI]\n  }\n}\n\nclient<llm> Openai {\n  provider fallback\n  options {\n    // This will try the clients in order until one succeeds\n    // Learn more at https://docs.boundaryml.com/docs/snippets/clients/fallback\n    strategy [GPT4, FastOpenAI]\n  }\n}",
    "generators.baml": "\n// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\"\n    output_type \"python/pydantic\"\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../\"\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.58.0\"\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    // Regardless of this setting, you can always explicitly call either of the following:\n    // - b.sync.FunctionName()\n    // - b.async_.FunctionName() (note the underscore to avoid a keyword conflict)\n    default_client_mode sync\n}   ",
}

def get_baml_files():
    return file_map