# Locator Naming Conventions

## General Rules

1. Use descriptive, meaningful names
2. Follow snake_case naming convention (Python standard)
3. Use consistent prefixes to indicate the type of element
4. Make locators private by using double underscore prefix (__)
5. Prioritize data-testid attributes when possible
6. Always place the element type prefix at the beginning of the name
7. If the element doesn't match any defined type, skip the prefix and use a descriptive name

## Common Prefixes

- `btn` - for buttons
- `txt` - for text fields/input fields
- `lbl` - for labels
- `lnk` - for links
- `img` - for images
- `chk` - for checkboxes
- `rdb` - for radio buttons
- `drp` - for dropdowns
- `tbl` - for tables
- `lst` - for lists
- `frm` - for forms
- `ico` - for icons
- `tab` - for tabs
- `opt` - for options
- `item` - for list items or generic items

## Examples

### Good Examples

```python
__txt_username = (By.CSS_SELECTOR, "input[data-testid='username']")
__tab_account_type = (By.CSS_SELECTOR, "*[data-testid='tab-login-account-type-{}']")
__opt_language = (By.CSS_SELECTOR, "li[data-testid='language-option']")
__item_user = (By.CSS_SELECTOR, "*[data-testid='user-list-item']")
```

### Bad Examples

```python
# Don't put type at the end
__username_txt = (By.CSS_SELECTOR, "input[data-testid='username']")
# Don't use generic names
__button1 = (By.CSS_SELECTOR, "button[data-testid='submit']")
# Don't omit type prefix
__user_id = (By.CSS_SELECTOR, "input[data-testid='user-id']")
```

## Best Practices

1. **Private Locators**: Use double underscore prefix to make locators private
2. **Use data-testid**: Prefer data-testid attributes for element selection
3. **Organize by Sections**: Use clear section comments to separate locators, actions, and verifications
   ```python
   # ------------------------ LOCATORS ------------------------ #
   # Locator definitions here
   
   # ------------------------ ACTIONS ------------------------ #
   # Action methods here
   
   # ------------------------ VERIFY ------------------------ #
   # Verification methods here
   ```
4. **Dynamic Locators**: Use helper functions for dynamic locators
   ```python
   # Good
   __drp_account_type = (By.CSS_SELECTOR, "*[data-testid='tab-login-account-type-{}']")
   
   def select_account_type(self, account_type: str):
       self.actions.click(cook_element(self.__drp_account_type, account_type.lower()))
   ```

## Locator Types Priority

1. data-testid (Most preferred)
2. id
3. name
4. CSS Selector
5. XPath (Least preferred, use only when necessary)
