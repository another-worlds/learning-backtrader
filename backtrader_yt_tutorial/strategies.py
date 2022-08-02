import backtrader

class TestStrategy_v1(backtrader.Strategy):
    
    # Logging func
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    # Keep a reference to a close
    def __init__(self):
        self.dataclose = self.datas[0].close
    
    def log_order(self, order):
        # IF order completed : activate logic
        if order.status in [order.Completed]:
            # If it's a buy order, record sell price
            if order.isbuy():
                self.log(f"BUY EXECUTED, {order.executed.price}")
                self.buy_date = len(self)
            if order.issell():
                self.log(f"SELL EXECUTED, {order.executed.price}")

        self.order = None


    def next(self):
        # Log the closing price of the series
        self.log('Close, %.2f' % self.dataclose[0])


        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:

                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()
                    self.log_order()
        else:   
            if len(self) >= self.buy_date + 5:
                self.log(f'SELL CREATE {self.dataclose[0]}' )
                self.order = self.sell()
        

class TestStrategy_v3(backtrader.Strategy):
    
    # Logging func
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    # Keep a reference to a close
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, {order.executed.price}")

            if order.issell():
                self.log(f"SELL EXECUTED, {order.executed.price}")
        
            self.bar_executed = len(self)
        self.order = None




    def next(self):
        # Log the closing price of the series
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:

                    self.log(f'BUY CREATE {self.dataclose[0]}')
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log(f'SELL CREATE {self.dataclose[0]}')
                self.order = self.sell()
        

