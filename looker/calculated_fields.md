# Calculated fields & metrics for Looker Studio

In Looker Studio: **Resource -> Manage added data sources -> Edit (on retail_clean) -> Add a field**.
Paste the name and formula. Set the type as noted. (Formulas use Looker Studio syntax.)

## First: fix field types (in the data source editor)
| Field | Set type to |
|---|---|
| `invoice_date` | Date & Time -> **Date (YYYYMMDD)** |
| `invoice_datetime` | Date & Time -> **Date Hour Minute (YYYYMMDDhhmm)** *or leave as Text - not required* |
| `year_month` | Text (used as a sortable label) |
| `customer_id`, `invoice_no`, `stock_code` | Text |
| `revenue`, `unit_price` | Number -> Currency (GBP) |
| `country` | Geo -> **Country** (enables the geo map) |
Default aggregation: `revenue` = Sum, `quantity` = Sum.

## Metrics (add as new fields in `retail_clean`)
| Field name | Formula | Type |
|---|---|---|
| Net Revenue | `SUM(CASE WHEN is_non_product = 0 THEN revenue ELSE 0 END)` | Currency |
| Gross Sales | `SUM(CASE WHEN is_cancellation = 0 AND is_non_product = 0 THEN revenue ELSE 0 END)` | Currency |
| Cancelled Value | `ABS(SUM(CASE WHEN is_cancellation = 1 THEN revenue ELSE 0 END))` | Currency |
| Cancellation Rate | `COUNT_DISTINCT(CASE WHEN is_cancellation = 1 THEN invoice_no END) / COUNT_DISTINCT(invoice_no)` | Percent |
| Orders | `COUNT_DISTINCT(CASE WHEN is_cancellation = 0 THEN invoice_no END)` | Number |
| Customers | `COUNT_DISTINCT(CASE WHEN customer_id != '' THEN customer_id END)` | Number |
| Average Order Value | `SUM(CASE WHEN is_cancellation = 0 AND is_non_product = 0 THEN revenue ELSE 0 END) / COUNT_DISTINCT(CASE WHEN is_cancellation = 0 THEN invoice_no END)` | Currency |
| Units Sold | `SUM(CASE WHEN is_cancellation = 0 AND is_non_product = 0 THEN quantity ELSE 0 END)` | Number |
| Revenue per Customer | `SUM(CASE WHEN is_cancellation = 0 AND is_non_product = 0 AND customer_id != '' THEN revenue ELSE 0 END) / COUNT_DISTINCT(CASE WHEN customer_id != '' THEN customer_id END)` | Currency |
| Guest Order Share | `COUNT_DISTINCT(CASE WHEN is_guest = 1 THEN invoice_no END) / COUNT_DISTINCT(invoice_no)` | Percent |
| International Share | `SUM(CASE WHEN is_uk = 0 AND is_cancellation = 0 AND is_non_product = 0 THEN revenue ELSE 0 END) / SUM(CASE WHEN is_cancellation = 0 AND is_non_product = 0 THEN revenue ELSE 0 END)` | Percent |

## Dimensions
| Field name | Formula |
|---|---|
| Day Part | `CASE WHEN hour < 9 THEN "1 Early (<9)" WHEN hour < 12 THEN "2 Morning" WHEN hour < 15 THEN "3 Lunch/Afternoon" WHEN hour < 18 THEN "4 Late afternoon" ELSE "5 Evening" END` |
| Weekday Label | `CONCAT(weekday_num, " ", weekday)` |
| Market | `CASE WHEN country = "United Kingdom" THEN "UK" WHEN country IN ("Germany","France","EIRE","Netherlands","Spain","Belgium","Switzerland","Portugal","Italy") THEN "Europe" ELSE "Rest of world" END` |
| Basket Size Band | `CASE WHEN quantity < 0 THEN "Return" WHEN quantity < 6 THEN "1-5" WHEN quantity < 25 THEN "6-24" ELSE "25+" END` |

## Parameters (interactive metric switcher)
Add **Parameter** `Metric Selector` (Text; allowed values: Revenue, Orders, Units). Then a field:
`Selected Metric` =
```
CASE WHEN Metric Selector = "Revenue" THEN Gross Sales
     WHEN Metric Selector = "Orders" THEN Orders
     ELSE Units Sold END
```
Add a **Drop-down list** control bound to the parameter; use `Selected Metric` in charts.

## Blended data (retail + RFM)
Add a chart -> Blend data -> **Join**: left `retail_clean`, right `rfm_customers`, join key `customer_id`, type **Left outer**.
Dimensions: `segment`, `country`; metrics: `Gross Sales`, `Customers`. This gives "Revenue by customer segment".
