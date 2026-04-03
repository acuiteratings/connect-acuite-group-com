from collections import defaultdict


DIFFICULTY_LABELS = {
    "amateur": "Amateur",
    "enthusiast": "Enthusiast",
    "professional": "Professional",
    "expert": "Expert",
}

CATEGORY_LABELS = {
    "business": "Business",
    "finance": "Finance",
    "banking": "Banking",
    "markets": "Markets",
    "economics": "Economics",
}

PROMPT_PREFIXES = [
    "",
    "Choose the correct answer: ",
    "Pick the right option: ",
    "Select the correct answer: ",
    "Identify the right answer: ",
]

BASE_QUESTIONS = [
    ("business", "amateur", "What does B2B stand for?", ["Business to Business", "Back to Bank", "Brand to Brand", "Business to Borrower"], 0),
    ("business", "amateur", "What is revenue?", ["Income from sales before expenses", "Profit after tax", "Cash in bank", "Money spent on salaries"], 0),
    ("business", "amateur", "What is a customer?", ["A buyer of a product or service", "Only a company owner", "A tax officer", "A shareholder"], 0),
    ("business", "amateur", "What does KPI commonly mean?", ["Key Performance Indicator", "Known Profit Index", "Key Payment Instruction", "Kind Process Input"], 0),
    ("business", "amateur", "What is market share?", ["A company's portion of total sales in a market", "A firm's bank balance", "A company's tax refund", "A loan repayment ratio"], 0),
    ("business", "enthusiast", "What is a value proposition?", ["The reason customers should choose a product", "A company's borrowing limit", "A tax planning method", "A dividend formula"], 0),
    ("business", "enthusiast", "What does CRM usually refer to?", ["Customer Relationship Management", "Corporate Revenue Manual", "Credit Risk Measure", "Current Ratio Model"], 0),
    ("business", "enthusiast", "What is an operating expense?", ["A cost of running the business", "A shareholder payout only", "A capital receipt", "A foreign exchange gain"], 0),
    ("business", "enthusiast", "What does procurement mean in business?", ["Purchasing goods or services", "Recruiting employees", "Raising equity capital", "Paying dividends"], 0),
    ("business", "enthusiast", "What is a brand in business terms?", ["The identity customers recognize and remember", "Only the company logo file", "A legal tax notice", "A warehouse document"], 0),
    ("business", "professional", "What does gross margin compare?", ["Gross profit with revenue", "Debt with equity", "Cash with inventory", "Tax with salary cost"], 0),
    ("business", "professional", "What is break-even point?", ["The level where total revenue equals total cost", "The day a company is listed", "A bonus declaration date", "The point where debt becomes equity"], 0),
    ("business", "professional", "What is working capital broadly about?", ["Short-term operating liquidity", "Long-term brand value", "Only equity capital", "Only tax deferred assets"], 0),
    ("business", "professional", "In operations, what does inventory turnover measure?", ["How quickly stock is sold and replaced", "How often employees are hired", "How frequently taxes are filed", "How often dividends are paid"], 0),
    ("business", "professional", "What is a business model?", ["How a company creates and earns value", "Its annual leave policy", "Its share certificate format", "Its tax audit schedule"], 0),
    ("business", "expert", "What does EBITDA exclude besides taxes?", ["Interest, depreciation and amortization", "Revenue and expenses", "Assets and liabilities", "Only cash balances"], 0),
    ("business", "expert", "What is vertical integration?", ["Controlling multiple stages of the value chain", "Selling only online", "Increasing office floors", "Hiring more managers"], 0),
    ("business", "expert", "What is customer churn?", ["The rate at which customers stop using a service", "The speed of product delivery", "The rate of tax change", "The stock market opening move"], 0),
    ("business", "expert", "What does SWOT include besides strengths and weaknesses?", ["Opportunities and threats", "Options and taxes", "Ownership and treasury", "Outsourcing and training"], 0),
    ("business", "expert", "What is a moat in business strategy?", ["A durable competitive advantage", "A large cash reserve", "A bond covenant", "A pricing error"], 0),

    ("finance", "amateur", "What does IPO stand for?", ["Initial Public Offering", "Internal Price Order", "Indexed Profit Output", "International Purchase Option"], 0),
    ("finance", "amateur", "What is a share?", ["A unit of ownership in a company", "A type of bank loan", "A tax receipt", "A bond coupon"], 0),
    ("finance", "amateur", "What is a dividend?", ["A payment made by a company to shareholders", "A company fine", "A tax on imports", "A bank processing fee"], 0),
    ("finance", "amateur", "Which statement shows profit or loss for a period?", ["Income statement", "Balance sheet", "Share certificate", "Audit memo"], 0),
    ("finance", "amateur", "What does profit after tax mean?", ["Earnings after taxes are deducted", "Sales before expenses", "Only cash collected", "Borrowings plus equity"], 0),
    ("finance", "enthusiast", "What is EPS?", ["Earnings per share", "Equity per sale", "Expense per stock", "Earnings payment system"], 0),
    ("finance", "enthusiast", "What does a balance sheet show?", ["Assets, liabilities and equity", "Only revenue and profit", "Only cash received", "Only tax provisions"], 0),
    ("finance", "enthusiast", "What is cash flow from operations about?", ["Cash generated by core business activity", "Money raised by loans only", "Tax paid on imports only", "Capital gains from stock sales"], 0),
    ("finance", "enthusiast", "What is debt?", ["Money borrowed that must be repaid", "Money paid as dividend", "A company's logo value", "Only retained earnings"], 0),
    ("finance", "enthusiast", "What does ROE measure?", ["Return on shareholders' equity", "Rate of export", "Revenue over expenses", "Risk of equity issue"], 0),
    ("finance", "professional", "What does P/E ratio compare?", ["Share price with earnings per share", "Profit with expenses", "Price with enterprise debt", "Promoter holding with earnings"], 0),
    ("finance", "professional", "What is free cash flow commonly used for?", ["Understanding cash left after core investments", "Measuring tax refunds only", "Counting employee leave", "Estimating office rent"], 0),
    ("finance", "professional", "What does current ratio compare?", ["Current assets with current liabilities", "Debt with equity", "Revenue with salary cost", "Operating cash with capex"], 0),
    ("finance", "professional", "What is depreciation?", ["Allocation of an asset's cost over time", "A tax penalty", "An equity issue", "A rise in inventory value"], 0),
    ("finance", "professional", "What is an annual report?", ["A yearly summary of financial and business performance", "A daily sales register", "A bank passbook", "A payroll slip"], 0),
    ("finance", "expert", "What does enterprise value broadly add to market capitalization?", ["Net debt and similar obligations", "Only dividends paid", "Only tax refunds", "Only cash sales"], 0),
    ("finance", "expert", "What is interest coverage ratio about?", ["Ability to service interest from earnings", "How often interest is revised", "The share of debt in equity", "The maturity of deposits"], 0),
    ("finance", "expert", "What is retained earnings?", ["Accumulated profit kept in the business", "Only fresh equity raised", "Only current year revenue", "Only loan proceeds"], 0),
    ("finance", "expert", "What is capex?", ["Spending on long-term assets", "Employee bonus expense", "Only interest payment", "Only tax deducted at source"], 0),
    ("finance", "expert", "What does net worth represent?", ["Assets minus liabilities", "Revenue minus tax", "Cash minus salary", "Profit minus dividend"], 0),

    ("banking", "amateur", "What does EMI stand for in retail lending?", ["Equated Monthly Instalment", "Estimated Money Index", "Equity Market Instruction", "Electronic Margin Item"], 0),
    ("banking", "amateur", "What is a savings account?", ["A deposit account for keeping money with a bank", "A kind of company share", "A tax filing format", "A warehouse register"], 0),
    ("banking", "amateur", "What is a loan?", ["Money borrowed that must be repaid", "A dividend payment", "A tax benefit", "A stock bonus"], 0),
    ("banking", "amateur", "What does KYC stand for?", ["Know Your Customer", "Keep Your Credit", "Key Yield Control", "Known Yearly Cost"], 0),
    ("banking", "amateur", "What is interest on a deposit?", ["The return a bank pays on deposited money", "A tax penalty", "A loan default fee", "An insurance premium"], 0),
    ("banking", "enthusiast", "What is collateral?", ["An asset pledged to secure a loan", "Only a customer's salary slip", "A type of tax refund", "A share buyback"], 0),
    ("banking", "enthusiast", "What does ATM stand for?", ["Automated Teller Machine", "Automated Transfer Method", "Account Tracking Monitor", "Any Time Moneyline"], 0),
    ("banking", "enthusiast", "What is CASA in banking?", ["Current and savings accounts", "Capital and secured assets", "Corporate account settlement agreement", "Credit allocation system area"], 0),
    ("banking", "enthusiast", "What does NEFT enable?", ["Electronic bank fund transfers", "Equity listing of companies", "Foreign exchange hedging", "Tax refund processing"], 0),
    ("banking", "enthusiast", "What is a fixed deposit?", ["A deposit kept for a set term at a stated rate", "A floating-rate bond", "A type of equity share", "A warehouse invoice"], 0),
    ("banking", "professional", "What is an NPA?", ["A loan where repayment is overdue beyond the prescribed period", "A new private account", "A tax credit entry", "A negotiated payment authority"], 0),
    ("banking", "professional", "What does CRR stand for in India?", ["Cash Reserve Ratio", "Credit Recovery Rate", "Capital Return Rule", "Current Risk Reserve"], 0),
    ("banking", "professional", "What does SLR stand for in Indian banking?", ["Statutory Liquidity Ratio", "Secured Lending Rate", "Systemic Loan Review", "State Liability Register"], 0),
    ("banking", "professional", "What is a moratorium in loan terms?", ["A temporary pause on repayment obligation", "Permanent waiver of all debt", "A penalty charge", "An insurance add-on"], 0),
    ("banking", "professional", "What is RTGS generally used for?", ["Real-time high-value fund transfer", "Retail tax generation service", "Rapid treasury guarantee system", "Risk transfer grading scale"], 0),
    ("banking", "expert", "What does provisioning for bad loans mean?", ["Setting aside money for expected credit losses", "Paying dividends early", "Raising share capital", "Reducing branch count"], 0),
    ("banking", "expert", "What is net interest margin?", ["Difference between interest earned and paid relative to assets", "Only deposit growth", "Only loan recovery rate", "A tax refund ratio"], 0),
    ("banking", "expert", "What is a correspondent bank used for?", ["Helping banks transact across borders or currencies", "Running payroll for companies", "Auditing stock exchanges", "Valuing corporate bonds"], 0),
    ("banking", "expert", "What is asset-liability management in banking about?", ["Managing maturity, rate and liquidity mismatch risks", "Hiring branch managers", "Selling insurance only", "Printing debit cards"], 0),
    ("banking", "expert", "What is a credit appraisal?", ["Evaluation of a borrower's repayment ability and risk", "A stock market listing review", "An insurance claim form", "A tax demand notice"], 0),

    ("markets", "amateur", "What is a bull market?", ["A market where prices are generally rising", "A market closed for holidays", "A market with no buyers", "A government bond issue"], 0),
    ("markets", "amateur", "What is a bear market?", ["A market where prices are generally falling", "A market with only bond trading", "A tax payment cycle", "A bank branch closure"], 0),
    ("markets", "amateur", "What is a stock exchange?", ["A marketplace where securities are traded", "A warehouse for goods", "A central bank office", "A tax tribunal"], 0),
    ("markets", "amateur", "What is a bond?", ["A debt instrument issued to raise money", "A type of equity share", "A dividend certificate", "A tax challan"], 0),
    ("markets", "amateur", "What is market capitalization?", ["Share price multiplied by number of shares", "Total company revenue", "Total debt outstanding", "Cash held by promoters"], 0),
    ("markets", "enthusiast", "What is a benchmark index?", ["A reference index tracking a market segment", "A company's internal scorecard", "A bank lending rate", "A tax collection target"], 0),
    ("markets", "enthusiast", "What does blue-chip stock usually mean?", ["A large, established and reputed company stock", "A penny stock", "A newly listed loss-making stock", "A government bond"], 0),
    ("markets", "enthusiast", "What is liquidity in markets?", ["Ease of buying or selling without major price impact", "The amount of cash in a wallet", "Only bank deposit growth", "A fixed dividend ratio"], 0),
    ("markets", "enthusiast", "What is the primary market?", ["Where new securities are issued first", "Where only used shares trade", "A government tax portal", "A market for agricultural goods"], 0),
    ("markets", "enthusiast", "What is the secondary market?", ["Where existing securities trade among investors", "Where only IPOs occur", "A banking audit forum", "A currency printing press"], 0),
    ("markets", "professional", "What is a rights issue?", ["An offer allowing existing shareholders to buy new shares", "A court order about ownership", "A loan waiver scheme", "A mutual fund merger"], 0),
    ("markets", "professional", "What is hedging?", ["Taking an offsetting position to reduce risk", "Buying only the riskiest stocks", "Paying dividends early", "Selling only in cash"], 0),
    ("markets", "professional", "What is a futures contract?", ["An agreement to buy or sell later at a preset price", "A dividend declaration note", "A tax demand notice", "A deposit receipt"], 0),
    ("markets", "professional", "What is an option premium?", ["The price paid to buy an option", "The dividend on preference shares", "The cost of a bond coupon", "The tax paid on gains"], 0),
    ("markets", "professional", "Bond prices and yields usually move in what way?", ["In opposite directions", "In the same direction always", "With no relationship", "Only upward together"], 0),
    ("markets", "expert", "What is arbitrage?", ["Profiting from price differences in two markets", "A bond default event", "A rights issue discount", "An insider trading penalty"], 0),
    ("markets", "expert", "What is bid-ask spread?", ["The gap between buyer and seller quoted prices", "The difference between revenue and profit", "The time between two trades", "The distance between exchanges"], 0),
    ("markets", "expert", "What is short selling?", ["Selling borrowed securities hoping to buy back lower", "Selling only long-term bonds", "Buying only falling stocks", "Selling shares to promoters only"], 0),
    ("markets", "expert", "What does duration measure in bonds?", ["Sensitivity of bond price to interest-rate changes", "The number of coupons remaining only", "The age of the bondholder", "The time to open a trading account"], 0),
    ("markets", "expert", "What is price discovery?", ["The market process of finding a fair trading price", "A tax audit on listed firms", "A regulator-set fixed price", "A company's annual budgeting step"], 0),

    ("economics", "amateur", "What is inflation?", ["A general rise in prices", "A general fall in prices", "A rise only in salaries", "A drop only in taxes"], 0),
    ("economics", "amateur", "What does GDP commonly measure?", ["Total economic output", "Only government salary spending", "Only exports", "Only industrial taxes"], 0),
    ("economics", "amateur", "What is demand?", ["Desire and ability to buy a good or service", "Only the price of a good", "Only the stock available", "Only the tax rate"], 0),
    ("economics", "amateur", "What is supply?", ["The amount producers are willing to sell", "The amount customers save", "The interest on loans", "The number of banks"], 0),
    ("economics", "amateur", "What is unemployment?", ["People willing to work but without jobs", "People changing cities", "People studying full-time", "People with overtime work"], 0),
    ("economics", "enthusiast", "If demand rises and supply stays unchanged, price usually what?", ["Rises", "Falls", "Becomes zero", "Stops changing permanently"], 0),
    ("economics", "enthusiast", "If supply rises and demand stays unchanged, price usually what?", ["Falls", "Rises", "Doubles automatically", "Becomes fixed forever"], 0),
    ("economics", "enthusiast", "What is fiscal deficit broadly the gap between?", ["Government spending and government receipts", "Exports and imports", "Savings and investment", "Assets and liabilities"], 0),
    ("economics", "enthusiast", "What is deflation?", ["A prolonged fall in overall prices", "A rise in fuel taxes only", "A rise in stock prices only", "A fall in exports only"], 0),
    ("economics", "enthusiast", "What is a budget surplus?", ["Receipts exceeding expenditure", "Expenditure exceeding receipts", "Zero inflation", "A current account deficit"], 0),
    ("economics", "professional", "What is repo rate in India broadly about?", ["The rate at which RBI lends to banks", "A long-term bond coupon", "A listed company's dividend rate", "The rate of GST refund"], 0),
    ("economics", "professional", "What is monetary policy mainly concerned with?", ["Managing money, credit and interest conditions", "Approving company mergers", "Drafting company HR policy", "Allocating office space"], 0),
    ("economics", "professional", "What is the CPI used for?", ["Tracking consumer price inflation", "Measuring company profits", "Counting bank branches", "Measuring stock turnover"], 0),
    ("economics", "professional", "What does elasticity of demand describe?", ["How demand responds to changes such as price", "How inflation affects savings only", "How taxes are collected", "How stock prices move every day"], 0),
    ("economics", "professional", "What is a subsidy?", ["Financial support intended to lower cost or support activity", "A tax penalty", "A listed company's bonus share", "A bank deposit type"], 0),
    ("economics", "expert", "What is opportunity cost?", ["The value of the next best alternative forgone", "Only the cash spent", "Only the time taken", "Only the tax paid"], 0),
    ("economics", "expert", "What is stagflation?", ["High inflation with weak growth and unemployment stress", "Fast growth with low inflation", "Only a stock market crash", "Only a currency appreciation"], 0),
    ("economics", "expert", "What is real GDP?", ["GDP adjusted for inflation", "GDP before tax", "GDP in foreign currency", "GDP of the private sector only"], 0),
    ("economics", "expert", "What is comparative advantage?", ["Benefit from specializing where opportunity cost is lower", "Advantage from having more money only", "Advantage from higher taxes", "Advantage from printing currency"], 0),
    ("economics", "expert", "What is current account deficit generally about?", ["Imports of goods, services and transfers exceeding corresponding inflows", "Government spending exceeding taxes", "A company paying high dividends", "Banks lending more than deposits"], 0),
]


def build_question_bank():
    questions = []
    by_difficulty = defaultdict(list)
    for base_index, (category, difficulty, prompt, options, answer_index) in enumerate(BASE_QUESTIONS, start=1):
        option_payload = [
            {"key": chr(65 + option_index), "label": option}
            for option_index, option in enumerate(options)
        ]
        correct_option = chr(65 + answer_index)
        for variant_index, prefix in enumerate(PROMPT_PREFIXES, start=1):
            key = f"{category}-{base_index:03d}-{variant_index}"
            full_prompt = f"{prefix}{prompt}".strip()
            question = {
                "key": key,
                "category": category,
                "difficulty": difficulty,
                "prompt": full_prompt,
                "options": option_payload,
                "correct_option": correct_option,
            }
            questions.append(question)
            by_difficulty[difficulty].append(question)
    return questions, by_difficulty


QUESTION_BANK, QUESTION_BANK_BY_DIFFICULTY = build_question_bank()
QUESTION_LOOKUP = {question["key"]: question for question in QUESTION_BANK}


def get_question_by_key(key):
    return QUESTION_LOOKUP[key]


def get_questions_for_difficulty(difficulty):
    return list(QUESTION_BANK_BY_DIFFICULTY.get(difficulty, []))
