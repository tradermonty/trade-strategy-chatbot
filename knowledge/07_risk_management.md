# Risk Management Strategy - リスク管理戦略

## Overview / 概要

Risk management is the cornerstone of successful investing and trading. This comprehensive guide covers portfolio-level risk management, position sizing, diversification strategies, and hedging techniques specifically for US stock market participants.

リスク管理は成功する投資とトレードの基礎です。本包括的ガイドでは、米国株式市場参加者向けのポートフォリオレベルのリスク管理、ポジションサイジング、分散戦略、ヘッジ手法を説明します。

## Fundamental Risk Management Principles / 基本的リスク管理原則

### Core Risk Principles
1. **Capital Preservation**: Protect principal before seeking returns
2. **Risk-Adjusted Returns**: Focus on return per unit of risk
3. **Downside Protection**: Limit maximum potential losses
4. **Diversification**: Don't put all eggs in one basket
5. **Position Sizing**: Risk appropriate amounts per position
6. **Time Horizon Alignment**: Match risk tolerance with investment timeline

### Risk vs Return Framework
- **Low Risk, Low Return**: Treasury bonds, money market funds
- **Medium Risk, Medium Return**: Diversified equity portfolios
- **High Risk, High Return**: Individual growth stocks, options
- **High Risk, Low Return**: Speculative trades, penny stocks (avoid)

## Types of Investment Risk / 投資リスクの種類

### Market Risk (Systematic Risk)
**Definition**: Risk affecting entire market or asset class
**Examples**:
- Economic recession
- Interest rate changes
- Geopolitical events
- Pandemic impacts

**Measurement**: Beta (β) relative to market
**Management**: Asset allocation, hedging strategies

### Specific Risk (Unsystematic Risk)
**Definition**: Risk specific to individual company or sector
**Examples**:
- Earnings disappointments
- Management changes
- Product recalls
- Competitive threats

**Measurement**: Standard deviation of excess returns
**Management**: Diversification across stocks and sectors

### Liquidity Risk
**Definition**: Difficulty selling positions quickly without price impact
**Factors**:
- Trading volume
- Bid-ask spreads
- Market cap size
- Crisis conditions

**Management**: 
- Focus on liquid securities (>$500M market cap)
- Maintain cash reserves
- Avoid illiquid investments during uncertainty

### Currency Risk
**Definition**: Impact of exchange rate changes on international investments
**Sources**:
- Foreign stock investments
- International ETFs
- Multinational companies

**Management**:
- Currency hedged ETFs (HEDJ, DXJ)
- Domestic focus during dollar strength
- Natural hedging through diversification

## Position Sizing Strategies / ポジションサイジング戦略

### The 1% Rule
**Principle**: Risk no more than 1% of portfolio per trade
**Calculation**: 
- Portfolio Value: $100,000
- Risk per Trade: $1,000 maximum
- If stop-loss is 10% below entry: Maximum position $10,000

### Kelly Criterion
**Formula**: f = (bp - q) / b
- f = fraction of capital to bet
- b = odds (reward/risk ratio)
- p = probability of winning
- q = probability of losing (1 - p)

**Example**:
- Win probability: 60%
- Average win: $300
- Average loss: $200
- Optimal position size: 5% of capital

### Equal Weight Strategy
**Approach**: Same dollar amount in each position
**Benefits**: 
- Simplicity
- Prevents over-concentration
- Systematic approach

**Drawbacks**:
- Ignores conviction levels
- May underweight best opportunities

### Risk Parity Approach
**Concept**: Equal risk contribution from each position
**Implementation**:
- Higher allocation to lower volatility stocks
- Lower allocation to higher volatility stocks
- Target 2-3% risk contribution per position

## Portfolio-Level Risk Management / ポートフォリオレベル・リスク管理

### Diversification Strategies

#### Geographic Diversification
- **US Large Cap**: 40-60% of equity allocation
- **US Mid/Small Cap**: 15-25% of equity allocation
- **International Developed**: 15-25% of equity allocation
- **Emerging Markets**: 5-15% of equity allocation

#### Sector Diversification
**Target Allocations** (vs S&P 500 weights):
- Technology: 20-30% (vs 28%)
- Healthcare: 10-15% (vs 13%)
- Financials: 8-15% (vs 13%)
- Consumer Discretionary: 8-15% (vs 11%)
- Communication Services: 5-10% (vs 8%)
- Consumer Staples: 5-10% (vs 6%)
- Industrials: 5-10% (vs 8%)
- Energy: 2-8% (vs 4%)
- Materials: 2-6% (vs 3%)
- Utilities: 2-6% (vs 3%)
- Real Estate: 2-6% (vs 3%)

#### Style Diversification
- **Growth vs Value**: 50-70% growth, 30-50% value
- **Large vs Small Cap**: 70-80% large cap, 20-30% small cap
- **Quality vs Momentum**: Balance based on market conditions

### Correlation Analysis
**Low Correlation Pairs** (<0.5):
- Utilities vs Technology
- Consumer Staples vs Consumer Discretionary
- REITs vs Growth Stocks
- Gold vs Stocks (negative correlation)

**High Correlation Risks** (>0.8):
- Technology stocks during sell-offs
- Financial stocks during credit stress
- Energy stocks during oil price moves
- All stocks during market crashes

### Value at Risk (VaR) Measurement
**Definition**: Maximum expected loss over specific time period at given confidence level

**Example Calculation** (95% confidence, 1 day):
- Portfolio value: $100,000
- Daily standard deviation: 1.5%
- 95% VaR = $100,000 × 1.65 × 1.5% = $2,475

**Applications**:
- Daily risk monitoring
- Position sizing decisions
- Stress testing portfolios

## Stop-Loss Strategies / ストップロス戦略

### Technical Stop-Loss Methods

#### 1. Percentage Stops
- **Conservative**: 5-8% below entry
- **Moderate**: 10-15% below entry
- **Aggressive**: 15-20% below entry

**Advantages**: Simple, systematic
**Disadvantages**: Ignores volatility differences

#### 2. Volatility-Based Stops
**Average True Range (ATR) Method**:
- Stop = Entry Price - (2 × ATR)
- Adjusts for stock's natural volatility
- More appropriate for different securities

#### 3. Support Level Stops
- Place stops below key support levels
- Allows for normal price fluctuations
- Requires technical analysis skills

### Trailing Stop Strategies

#### 1. Fixed Percentage Trailing
- Move stop up as price rises
- Maintain fixed percentage below high
- Example: 15% trailing stop

#### 2. ATR Trailing Stops
- Use 2-3× ATR below highest high
- Adapts to changing volatility
- More sophisticated approach

#### 3. Moving Average Stops
- Stop below 20-day or 50-day MA
- Dynamic adjustment to trend
- Trend-following approach

### Mental vs Mechanical Stops
**Mechanical Stops**:
- Automatically executed orders
- Removes emotional decisions
- May trigger on temporary spikes

**Mental Stops**:
- Discretionary decision-making
- Allows for fundamental review
- Requires discipline to execute

## Hedging Strategies / ヘッジ戦略

### Options-Based Hedging

#### 1. Protective Puts
**Strategy**: Buy puts on individual stocks or ETFs
**Cost**: 1-3% of position value (quarterly)
**Protection**: Limits downside to put strike price

**Example**:
- Own 100 shares SPY at $400
- Buy $380 put for $8
- Maximum loss: $28 per share (7%)

#### 2. Collar Strategy
**Strategy**: Own stock + protective put + covered call
**Cost**: Net credit or small debit
**Trade-off**: Limited upside for downside protection

**Example**:
- Own stock at $100
- Buy $95 put for $3
- Sell $110 call for $2
- Net cost: $1, protection below $94

#### 3. Portfolio Hedging
**VIX Calls**: Profit from volatility spikes
**SPY Puts**: Direct index hedging
**Inverse ETFs**: SH (short S&P), PSQ (short QQQ)

### Sector Hedging Strategies

#### 1. Long/Short Pairs
- Long strong stock, short weak stock in same sector
- Reduces sector risk, isolates stock selection
- Example: Long AAPL, Short older tech stock

#### 2. Sector ETF Hedging
- Short sector ETF against individual stock positions
- Hedge sector-specific risks
- Maintain stock-specific alpha opportunity

### Currency Hedging
**Currency Hedged ETFs**:
- HEDJ: Europe hedged
- DXJ: Japan hedged
- DBEF: Developed markets ex-US hedged

**Benefits**: Eliminates currency risk
**Costs**: Hedging fees (0.3-0.5% annually)

## Risk Monitoring and Measurement / リスク監視・測定

### Daily Risk Metrics

#### 1. Portfolio Beta
**Calculation**: Weighted average of individual stock betas
**Target Range**: 0.8-1.2 for diversified portfolios
**Interpretation**: Sensitivity to market movements

#### 2. Concentration Risk
**Single Stock Limit**: Maximum 5-8% of portfolio
**Sector Limits**: Maximum 25-30% in any sector
**Geographic Limits**: Maximum 70% in single country

#### 3. Liquidity Assessment
**Daily Volume**: Minimum $1M average daily volume
**Market Cap**: Minimum $500M for core holdings
**Bid-Ask Spread**: <0.5% for liquid securities

### Weekly Risk Review

#### 1. Correlation Analysis
- Monitor changing correlations
- Identify crowded trades
- Assess diversification effectiveness

#### 2. Drawdown Analysis
- Current drawdown from peak
- Historical maximum drawdowns
- Recovery time analysis

#### 3. Risk-Adjusted Performance
**Sharpe Ratio**: (Return - Risk-free rate) / Standard deviation
**Sortino Ratio**: Focuses on downside deviation only
**Calmar Ratio**: Annual return / Maximum drawdown

### Monthly Risk Assessment

#### 1. Stress Testing
**Market Scenarios**:
- 10% market decline
- 20% market decline
- 2008-style crisis
- Sector-specific shocks

#### 2. Portfolio Rebalancing
- Return to target allocations
- Trim outperforming positions
- Add to underperforming positions

## Crisis Risk Management / 危機時リスク管理

### Market Crash Protocols

#### Phase 1: Initial Response (0-48 hours)
1. **Assess Damage**: Calculate portfolio impact
2. **Review Stops**: Honor predetermined exit rules
3. **Preserve Cash**: Avoid panic buying
4. **Stay Disciplined**: Follow risk management plan

#### Phase 2: Evaluation (1-2 weeks)
1. **Fundamental Review**: Assess if thesis intact
2. **Liquidity Check**: Ensure adequate cash reserves
3. **Opportunity Assessment**: Identify potential bargains
4. **Risk Capacity**: Review risk tolerance

#### Phase 3: Recovery Positioning (2-8 weeks)
1. **Gradual Re-entry**: Dollar-cost average back in
2. **Quality Focus**: Emphasize strong balance sheets
3. **Diversification**: Maintain broad diversification
4. **Patience**: Allow time for recovery

### Black Swan Event Management
**Characteristics**: Unpredictable, extreme impact events
**Examples**: 
- COVID-19 pandemic
- 9/11 attacks
- Flash crashes
- Geopolitical crises

**Preparation Strategies**:
- Maintain 10-20% cash reserves
- Diversify across asset classes
- Use options for tail protection
- Have predetermined action plans

## Psychological Risk Management / 心理的リスク管理

### Emotional Risk Factors

#### 1. Fear of Missing Out (FOMO)
**Symptoms**: Chasing performance, over-trading
**Management**: Stick to investment process, maintain discipline

#### 2. Loss Aversion
**Symptoms**: Holding losers too long, selling winners too early
**Management**: Predetermined exit rules, systematic rebalancing

#### 3. Confirmation Bias
**Symptoms**: Seeking information that confirms positions
**Management**: Devil's advocate analysis, diverse information sources

### Behavioral Risk Controls

#### 1. Investment Policy Statement
- Written investment objectives
- Risk tolerance documentation
- Asset allocation targets
- Rebalancing rules

#### 2. Decision Journals
- Record investment rationale
- Track decision outcomes
- Learn from mistakes
- Identify behavioral patterns

#### 3. Systematic Processes
- Regular review schedules
- Predetermined criteria for buying/selling
- Mechanical rebalancing rules
- External accountability (advisor/peer group)

## Risk Management Tools and Technology / リスク管理ツール・技術

### Portfolio Management Software
1. **Personal Capital**: Free portfolio tracking
2. **Morningstar Portfolio Manager**: Professional analysis
3. **YCharts**: Institutional-quality tools
4. **Bloomberg Terminal**: Professional standard

### Risk Metrics Monitoring
- **Beta calculation**: Portfolio vs market sensitivity
- **Correlation matrices**: Inter-asset relationships
- **VaR calculations**: Potential loss estimates
- **Stress testing**: Scenario analysis tools

### Automated Risk Controls
- **Stop-loss orders**: Automatic execution
- **Position sizing calculators**: Risk-based allocation
- **Rebalancing alerts**: Deviation notifications
- **Correlation monitoring**: Crowding warnings

## Common Risk Management Mistakes / 一般的リスク管理の間違い

### Planning Mistakes
1. **No written plan**: Flying blind without strategy
2. **Unrealistic expectations**: Over-optimistic assumptions
3. **Inadequate diversification**: Too concentrated
4. **Ignoring correlations**: False diversification

### Execution Mistakes
1. **Moving stops**: Changing rules mid-game
2. **Position sizing errors**: Risking too much
3. **Emotional decisions**: Overriding systematic approach
4. **Neglecting monitoring**: Set-and-forget mentality

### Recovery Mistakes
1. **Revenge trading**: Trying to make back losses quickly
2. **Abandoning strategy**: Changing approach after losses
3. **Insufficient cash**: No dry powder for opportunities
4. **Panic selling**: Crystallizing losses at worst times

## Risk Management Checklist / リスク管理チェックリスト

### Daily Tasks
- [ ] Monitor portfolio value and major positions
- [ ] Check for stop-loss triggers
- [ ] Review market news and developments
- [ ] Assess liquidity needs

### Weekly Tasks
- [ ] Calculate portfolio beta and correlations
- [ ] Review sector and geographic allocations
- [ ] Analyze risk-adjusted performance metrics
- [ ] Update risk monitoring spreadsheets

### Monthly Tasks
- [ ] Conduct full portfolio review
- [ ] Rebalance to target allocations
- [ ] Stress test portfolio scenarios
- [ ] Review and update investment policy statement

### Quarterly Tasks
- [ ] Comprehensive risk assessment
- [ ] Review and adjust risk management strategies
- [ ] Analyze behavioral patterns and mistakes
- [ ] Update long-term investment goals

## Key Takeaways / 重要ポイント

1. **Risk First**: Always consider risk before return potential
2. **Systematic Approach**: Follow predetermined rules and processes
3. **Diversification**: Spread risk across multiple dimensions
4. **Position Sizing**: Risk appropriate amounts per position
5. **Monitoring**: Continuously track and adjust risk exposures
6. **Discipline**: Stick to the plan during emotional market periods
7. **Learning**: Continuously improve risk management practices