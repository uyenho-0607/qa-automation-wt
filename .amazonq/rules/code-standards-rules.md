# Code Standards

## General

- PEP 8 Compliance
  - The codebase adheres to Python PEP 8 style conventions.
- Line Length
  - Limited to 200 characters
- Unused Code Cleanup
  - Remove unused imports and variables, excessive blank lines.
- Type Hints
  - Use type hints consistently for parameters and return types.

## Function & Parameter Design

- Simple Functions
  - Include brief docstrings (purpose only).
  - Skip parameter explanations unless non-obvious.
- Complex Functions
  - Include detailed docstrings and inline comments explaining business logic.
  ```python
  def calculate_trade_parameters(
          live_price: str | float,
          trade_type: TradeType = TradeType.BUY,
          order_type: OrderType = OrderType.MARKET,
          sl_type: SLTPType | str = SLTPType.PRICE,
          tp_type: SLTPType | str = SLTPType.PRICE,
          invalid: bool = False,
  ) -> DotDict[Any, Any]:
      """
      Calculate trade parameters for order placement.
      
      Args:
          live_price: Current market price
          trade_type: BUY or SELL
          order_type: MARKET, LIMIT, STOP, or STOP_LIMIT
          sl_type: PRICE or POINTS for stop loss calculation
          tp_type: PRICE or POINTS for take profit calculation
          invalid: If True, generates invalid prices for testing
      
      Returns:
          DotDict with entry_price, stop_limit_price, stop_loss, take_profit
      """
      prices = _calculate_trade_price(live_price, trade_type, order_type, invalid)

      live_price = prices.stop_limit_price or prices.entry_price
      sl_tp_points = _random_sl_tp_points(live_price, trade_type)

      return DotDict(
          entry_price=prices.entry_price,
          stop_limit_price=prices.stop_limit_price,
          stop_loss=(prices if sl_type == SLTPType.PRICE else sl_tp_points).stop_loss,
          take_profit=(prices if tp_type == SLTPType.PRICE else sl_tp_points).take_profit,
      )
  ```
- Function Parameters
  - 5+ parameters - all or non-obvious must be clearly documented
  - 8+ parameters - should use a custom Object/dictionary or dataclass to group related parameters.
  ```python
  def place_order(
            self,
            trade_object: ObjectTrade,
            sl_type: SLTPType = SLTPType.PRICE,
            tp_type: SLTPType = SLTPType.PRICE,
            swap_to_units: bool = False,
            submit: bool = False,
    ) -> None:
        """
        Place a valid order and load input data into trade_object.
        Args:
            trade_object: Should contain trade_type and order_type
            sl_type: Type of stop loss (PRICE/POINTS)
            tp_type: Type of take profit (PRICE/POINTS)
            swap_to_units: Whether to swap to units display
            submit: Whether to submit trade confirmation modal
        :returns: None
        """
        trade_type, order_type = trade_object.trade_type, trade_object.order_type
        # Select trade type and order type
        self._select_trade_type(trade_type)
        self._select_order_type(order_type)

        # Handle volume display
        not swap_to_units or self.swap_to_units()

        # Input volume and get units
        volume = self._input_volume()
        units = volume / trade_object.CONTRACT_SIZE if trade_object.CONTRACT_SIZE else self._get_volume_info_value()

        # Calculate trade parameters
        params = calculate_trade_parameters(
            self.get_live_price(trade_type), trade_type, order_type, sl_type=sl_type, tp_type=tp_type
        )

        # Input prices
        self._input_price(params.entry_price, order_type)
        self._input_stop_limit_price(params.stop_limit_price, order_type)
        self.actions.scroll_down(amount=1)  # scroll down a bit
  ```
## Logging Levels

- Use `logger.debug()` for internal traces and low-level technical steps.
- Use `logger.info()` Key user actions, test steps, and verifications.
- Use `logger.warning()` Unexpected but non-blocking issues (e.g., retry attempts, missing optional data) – for debugging purposes if needed
- Use `logger.error()` for actual errors or test failures
  ```python
     def _select_expiry(self, expiry: Expiry | str) -> Optional[str]:
        """Select expiry for the order. Return selected expiry"""
        if expiry:
            logger.debug(f"- Select expiry: {expiry.capitalize()!r}")
            self.actions.click(self.__drp_expiry)
            self.actions.click(cook_element(self.__opt_expiry, expiry.lower()))
            if expiry in [Expiry.SPECIFIED_DATE, Expiry.SPECIFIED_DATE_TIME]:
                logger.debug(f"- Select expiry date")
                self.actions.scroll_down()
                self.actions.click(self.__expiry_date)
self.actions.swipe_picker_wheel_down(self.__wheel_expiry_date)
                self.click_confirm_btn()
            return expiry
        return None
  ```

  ```python
  def test(web, symbol, get_asset_tab_amount, sl_type, tp_type):
    trade_object = ObjectTrade(order_type=OrderType.MARKET, symbol=symbol)
    tab_amount = get_asset_tab_amount(trade_object.order_type)

    logger.info(f"Step 1: Place {trade_object.trade_type} order with sl_type: {sl_type!r}, tp_type: {tp_type!r}")
    web.trade_page.place_order_panel.place_order(trade_object, sl_type=sl_type, tp_type=tp_type)

    logger.info("Verify trade confirmation modal information is correct")
    web.trade_page.modals.verify_trade_confirmation(trade_object)
  ```

## Code Organisation

- Private Locators: Prefix with double underscore (e.g. `__btn_login.`)
- Protected methods: for internal methods with a single underscore (e.g. `select_price`), signaling that these methods should not be used in test files.
- Section Comments: For page objects classes:
  ```python
  # ------------------------ LOCATORS ------------------------ #
  # ------------------------ ACTIONS ------------------------ #
  # ------------------------ VERIFY ------------------------ #
  ```

## Naming conventions

- Test files: `test_[MODULE_PREFIX]_TC[XX]_[positive|negative]_[description].py`
  - e.g. `test_TRD_MRK_TC01_positive_place_order.py`
- Functions: snake_case (`place_order`)
- Classes: PascalCase (`BasePage`, `LoginPage`)
- Constants: UPPER_CASE (`EXPLICIT_WAIT`)
- Locators: Descriptive with prefixes (`__btn_login`, `__txt_username`)
