# Permissions and Groups Setup

## Custom Permissions Added
Defined in `Book` model:
- can_view
- can_create
- can_edit
- can_delete

## Groups Created
- **Viewers**: has `can_view`
- **Editors**: has `can_view`, `can_create`, `can_edit`
- **Admins**: all permissions

## Views Protection
- All actions (view, create, edit, delete) are protected using `@permission_required`.

## Testing
Create test users and assign to groups via Django admin to verify permissions.

