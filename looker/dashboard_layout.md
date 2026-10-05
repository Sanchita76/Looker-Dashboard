# Dashboard layout - 3 pages  (canvas: Theme and layout -> Layout -> Grid, 1200 x 900 px)

**Theme:** Theme and layout -> Theme -> Customize: Background `#F5F7FB`, Text `#1F2A44`, Primary `#1A73E8`,
accent colours `#34A853, #F9AB00, #EA4335, #9334E6`. Font: Roboto. Add a header rectangle (dark blue `#1F2A44`) with a title text.
Add to every page: **Date range control** (default: Custom = full data range; data is 2010-12 to 2011-12), **Drop-down** `country`,
and a **Filter control** `description` (product search). Use Page -> *Report-level* for the header so controls persist.

## Page 1 - Sales Overview  (data source: retail_clean)
| # | Chart | Dimension | Metric | Notes |
|---|---|---|---|---|
| 1-5 | **Scorecards** (x5) | - | `Gross Sales`, `Orders`, `Customers`, `Average Order Value`, `Cancellation Rate` | enable "Comparison date range: Previous period" to show delta arrows |
| 6 | **Time series** | `invoice_date` (Day/Month) | `Gross Sales` (+ optional `Orders` on right axis) | Style: smoothing on, trend line |
| 7 | **Bar chart** (horizontal) | `description` | `Gross Sales` | Rows 10, sort Gross Sales desc, title "Top 10 products" |
| 8 | **Geo map** (filled) | `country` | `Gross Sales` | Zoom Europe/World |
| 9 | **Donut** | `Market` | `Gross Sales` | |
| 10 | **Table with heatmap** | `country` | `Gross Sales`, `Orders`, `Average Order Value` | Style: heatmap on Gross Sales, Rows per page 10 |

## Page 2 - Customer Behaviour  (data: retail_clean + blend with rfm_customers)
| # | Chart | Dimension | Metric |
|---|---|---|---|
| 1 | **Pivot table with heatmap** | rows `weekday_label`, columns `hour` | `Orders` |
| 2 | **Column chart** | `Day Part` | `Gross Sales` |
| 3 | **Treemap / Donut** (blend) | `segment` | `Customers` |
| 4 | **Bar chart** (blend) | `segment` | `Gross Sales` |
| 5 | **Scatter** (source: `rfm_customers`) | Dimension `customer_id`; X `frequency`, Y `monetary`, colour `segment` | - |
| 6 | **Scorecards** (rfm_customers) | `Average of recency_days`, `Average of frequency`, `Average of avg_order_value` | |
| 7 | **Table** (rfm_customers) | `customer_id`, `country`, `segment`, `recency_days`, `frequency`, `monetary` | sort `monetary` desc, add **bar** style on monetary |
Add a **Filter control** on `segment` that only affects this page.

## Page 3 - Products & Returns  (retail_clean, product_summary)
| # | Chart | Dimension | Metric |
|---|---|---|---|
| 1 | **Table** (product_summary) | `description` | `units`, `revenue`, `orders`, `customers`, `avg_price` (sortable, 15 rows) |
| 2 | **Bubble/Scatter** (product_summary) | `description`; X `avg_price`, Y `units`, size `revenue` | |
| 3 | **Bar chart** | `description` | `Cancelled Value` (top 10 most returned) |
| 4 | **Time series** | `invoice_date` | `Cancellation Rate` |
| 5 | **Column chart** | `Basket Size Band` | `Orders` |
| 6 | **Area chart** | `year_month` | `Gross Sales` by `Market` (breakdown dimension) |

## Polish
* Insert -> **Image/Text** for section headings; align with *Arrange -> Align*.
* Use **Chart interactions**: Report settings -> enable "Cross-filtering" so clicking a bar filters the page.
* Add **Data control**: Add a control -> Data control to let viewers switch the time-series metric (`Selected Metric` parameter).
* Share: **Share -> Invite people / Get report link**; schedule email delivery: Share -> Schedule delivery.
* Embed: File -> Embed report (enable embedding first).
