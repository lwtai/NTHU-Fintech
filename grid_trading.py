from typing import Dict, Any

class Strategy(StrategyBase):
    def __init__(self):
        # strategy attributes
        self.period = 60
        self.subscribed_books = {}
        self.options = {}

        # state tracking
        self.accumulated_gap = 0
        self.previous_gap = 0
        self.is_initialized = True
        self.should_stop_trading = False

        # parameters
        self.trade_unit = 1
        self.ceiling = 31000
        self.floor = 25000
        self.grid_gap = 500
        self.target_profit_pct = 0.25

    def on_order_state_change(self, order):
        exchange, pair, base, quote = CA.get_exchange_pair()
        quote_balance = CA.get_balance(exchange, quote)
        base_balance = CA.get_balance(exchange, base)
        CA.log(f'Balance - {quote}: {quote_balance.available}, {quote_balance.total}')

    def initialize_trading(self):
        exchange, pair, base, quote = CA.get_exchange_pair()
        leverage = CA.get_leverage()
        CA.log(f'{base}-{quote}, leverage: {leverage}')
        CA.open_long(exchange, pair, 6, CA.OrderType.MARKET)
        self.is_initialized = True

    def manage_positions(self, exchange, pair, close_price):
        if close_price > self.ceiling or close_price < self.floor:
            return

        while self.accumulated_gap >= self.grid_gap:
            CA.log('Sell BTC')
            long_position = CA.get_position(exchange, pair, CA.PositionSide.LONG)
            
            if long_position:
                CA.close_long(exchange, pair, self.trade_unit, CA.OrderType.MARKET)
            else:
                CA.open_short(exchange, pair, self.trade_unit, CA.OrderType.MARKET)
            
            self.accumulated_gap -= self.grid_gap

        while self.accumulated_gap <= -self.grid_gap:
            CA.log('Buy BTC')
            short_position = CA.get_position(exchange, pair, CA.PositionSide.SHORT)
            
            if short_position:
                CA.close_short(exchange, pair, self.trade_unit, CA.OrderType.MARKET)
            else:
                CA.open_long(exchange, pair, self.trade_unit, CA.OrderType.MARKET)
            
            self.accumulated_gap = -(abs(self.accumulated_gap) - self.grid_gap)

    def close_all_positions(self, exchange, pair):
        long_position = CA.get_position(exchange, pair, CA.PositionSide.LONG)
        short_position = CA.get_position(exchange, pair, CA.PositionSide.SHORT)
        
        if long_position:
            CA.close_long(exchange, pair, long_position.total_size, CA.OrderType.MARKET)
        if short_position:
            CA.close_short(exchange, pair, short_position.total_size, CA.OrderType.MARKET)

    def trade(self, candles):
        exchange, pair, base, quote = CA.get_exchange_pair()
        quote_balance = CA.get_balance(exchange, quote)
        
        if not self.is_initialized:
            self.initialize_trading()
            return
            
        if self.should_stop_trading:
            self.close_all_positions(exchange, pair)
            return
            
        profit = quote_balance.total - 100000
        if profit > 100000 * self.target_profit_pct:
            CA.log('Profit target reached')
            self.should_stop_trading = True
            return
            
        latest_candle = candles[exchange][pair][0]
        open_price = latest_candle['open']
        close_price = latest_candle['close']
        
        price_change = close_price - open_price
        self.accumulated_gap = self.previous_gap + price_change
        
        self.manage_positions(exchange, pair, close_price)
        self.previous_gap = self.accumulated_gap