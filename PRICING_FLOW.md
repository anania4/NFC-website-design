# Dynamic Pricing System Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Django Admin Panel                       │
│                  (http://localhost:8000/admin/)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Admin manages pricing
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   CardPricing Model                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │ • plan_type (individual, sm_business, etc.)        │    │
│  │ • name ("Individual")                              │    │
│  │ • subtitle ("Perfect for professionals")          │    │
│  │ • price (3900.00)                                  │    │
│  │ • card_range ("1-9 Cards")                         │    │
│  │ • features (multi-line text)                       │    │
│  │ • is_featured (Best Value badge)                   │    │
│  │ • is_popular (Most Popular badge)                  │    │
│  │ • display_order (1, 2, 3, 4)                       │    │
│  │ • is_active (show/hide)                            │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Database query
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   CardDetailView                             │
│  pricing_plans = CardPricing.objects.filter(                │
│      is_active=True                                          │
│  ).order_by('display_order')                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Pass to template
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              card_detail.html Template                       │
│  {% for plan in pricing_plans %}                            │
│      Display: name, price, features, badges                 │
│  {% endfor %}                                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Rendered HTML
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    User's Browser                            │
│  Displays pricing cards with current data from database     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Initial Setup
```
Developer runs:
  python manage.py migrate
  python manage.py populate_pricing
       ↓
Creates CardPricing table
       ↓
Populates 4 default plans
       ↓
Ready for admin management
```

### 2. Admin Updates Pricing
```
Admin logs into /admin/
       ↓
Navigates to Card Pricing
       ↓
Edits a plan (e.g., changes price from 3900 to 4200)
       ↓
Clicks Save
       ↓
Database updated immediately
       ↓
Next page load shows new price
```

### 3. User Views Pricing
```
User visits /card-detail/
       ↓
CardDetailView.get() called
       ↓
Queries CardPricing.objects.filter(is_active=True)
       ↓
Orders by display_order
       ↓
Passes to template as 'pricing_plans'
       ↓
Template loops through plans
       ↓
Renders HTML with current pricing
       ↓
User sees up-to-date pricing
```

## Admin Panel Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Admin Panel Home                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  CHECKOUT Section                            │
│  • Card Pricing  ← Click here                               │
│  • Checkout submissions                                      │
│  • Social media links                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Card Pricing List View                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Name      | Price    | Range    | Badges | Active  │    │
│  │ Individual| 3,900 Birr| 1-9 Cards| POPULAR| ✓      │    │
│  │ S&M Biz   | 3,600 Birr| 10-24    | -      | ✓      │    │
│  │ Enterprise| 3,200 Birr| 25-49    | -      | ✓      │    │
│  │ Corporate | 2,500 Birr| 50+      |FEATURED| ✓      │    │
│  └────────────────────────────────────────────────────┘    │
│  [Add Card Pricing] button                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Edit Card Pricing Form                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Basic Information                                   │    │
│  │  Plan type: [individual ▼]                         │    │
│  │  Name: [Individual                ]                │    │
│  │  Subtitle: [Perfect for professionals]             │    │
│  │  Price: [3900.00]                                  │    │
│  │  Card range: [1-9 Cards]                           │    │
│  │                                                     │    │
│  │ Features                                            │    │
│  │  [Customized Design                ]               │    │
│  │  [2 Year Subscription              ]               │    │
│  │  [Digital Profile                  ]               │    │
│  │  [Analytics Dashboard              ]               │    │
│  │                                                     │    │
│  │ Display Options                                     │    │
│  │  ☑ Is popular (Most Popular badge)                │    │
│  │  ☐ Is featured (Best Value badge)                 │    │
│  │  Display order: [1]                                │    │
│  │  ☑ Is active                                       │    │
│  │                                                     │    │
│  │  [Save] [Save and continue] [Save and add another] │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Feature Management

### Adding a Feature
```
1. Edit plan in admin
2. Go to Features field
3. Add new line: "New Feature Name"
4. Save
5. Feature appears on website immediately
```

### Removing a Feature
```
1. Edit plan in admin
2. Go to Features field
3. Delete the line
4. Save
5. Feature removed from website immediately
```

### Example Features Field
```
┌─────────────────────────────────┐
│ Customized Design               │
│ 2 Year Subscription             │
│ Digital Profile                 │
│ Analytics Dashboard             │
│ Priority Support                │
│ Dedicated Account Manager       │
└─────────────────────────────────┘
```

## Badge Logic

```
if plan.is_popular:
    Show "Most Popular" badge (yellow)
elif plan.is_featured:
    Show "Best Value" badge (green)
else:
    No badge
```

## Display Order Logic

```
Plans sorted by display_order (ascending):

display_order: 1 → First position (leftmost)
display_order: 2 → Second position
display_order: 3 → Third position
display_order: 4 → Fourth position (rightmost)

On mobile: Stacks vertically in same order
```

## Active/Inactive Logic

```
is_active = True  → Plan visible on website
is_active = False → Plan hidden (but kept in database)
```

## Database Schema

```
CardPricing Table
┌─────────────────┬──────────────┬──────────────┬──────────┐
│ Field           │ Type         │ Constraints  │ Default  │
├─────────────────┼──────────────┼──────────────┼──────────┤
│ id              │ BigAutoField │ Primary Key  │ Auto     │
│ plan_type       │ CharField(20)│ Unique       │ Required │
│ name            │ CharField    │ -            │ Required │
│ subtitle        │ CharField    │ -            │ Required │
│ price           │ Decimal(10,2)│ -            │ Required │
│ card_range      │ CharField(50)│ -            │ Required │
│ features        │ TextField    │ -            │ Default  │
│ is_featured     │ Boolean      │ -            │ False    │
│ is_popular      │ Boolean      │ -            │ False    │
│ display_order   │ Integer      │ -            │ 0        │
│ is_active       │ Boolean      │ -            │ True     │
│ created_at      │ DateTime     │ Auto         │ Now      │
│ updated_at      │ DateTime     │ Auto         │ Now      │
└─────────────────┴──────────────┴──────────────┴──────────┘
```

## Integration with Checkout

```
User clicks "Get Started" on a plan
       ↓
URL: /checkout/?plan=individual
       ↓
CheckoutView receives plan parameter
       ↓
Can use plan_type to pre-fill form or fetch price
       ↓
User completes checkout
       ↓
Order saved with selected plan
```

## Maintenance Commands

### Populate Initial Data
```bash
python manage.py populate_pricing
```
Creates/updates all 4 default plans

### Clean Up Old Orders
```bash
python manage.py cleanup_pending_orders --hours 24
```
Removes unpaid orders older than 24 hours

## Quick Reference

| Task | Steps |
|------|-------|
| Change price | Admin → Card Pricing → Edit plan → Update price → Save |
| Add feature | Admin → Card Pricing → Edit plan → Add line in Features → Save |
| Hide plan | Admin → Card Pricing → Edit plan → Uncheck "Is active" → Save |
| Reorder plans | Admin → Card Pricing → Edit each plan → Set display_order → Save |
| Add badge | Admin → Card Pricing → Edit plan → Check badge option → Save |

## Summary

The dynamic pricing system provides a complete solution for managing card pricing without code changes. All updates are immediate and reflected on the website in real-time.
