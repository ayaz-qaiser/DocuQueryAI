# DocuQuery AI - Tenancy and RBAC

## Overview

DocuQuery AI implements a comprehensive multi-tenant architecture with role-based access control (RBAC) to ensure proper data isolation and security across different organizations.

## Multi-Tenancy Architecture

### Tenant Identification
- **Header-based routing**: All API requests must include `X-Tenant-ID` header
- **Tenant validation**: Middleware validates tenant ID against active tenant registry
- **Fallback handling**: Requests without tenant ID are rejected with appropriate error

### Data Isolation Strategies
- **Database-level**: Tenant-specific schemas or tenant_id filtering
- **Cache isolation**: Redis keys prefixed with tenant identifier
- **File storage**: Separate directories per tenant in storage systems
- **Vector databases**: Qdrant collections scoped to tenant

### Tenant Configuration
```json
{
  "tenant_id": "acme_corp",
  "name": "Acme Corporation",
  "status": "active",
  "features": {
    "multi_tenancy": true,
    "oauth2": true,
    "document_ocr": true,
    "vector_search": true,
    "streaming": false
  },
  "limits": {
    "max_users": 1000,
    "max_documents": 10000,
    "max_storage_gb": 100,
    "rate_limit_per_user": 100
  },
  "settings": {
    "default_language": "en",
    "timezone": "America/New_York",
    "retention_days": 365
  }
}
```

## Role-Based Access Control (RBAC)

### Role Hierarchy
```
Super Admin (Global)
├── Tenant Admin
│   ├── Tenant Manager
│   ├── Security Admin
│   └── Billing Admin
├── User Manager
│   ├── User
│   └── Guest
└── System Admin
    ├── DevOps Engineer
    └── Support Engineer
```

### Role Definitions

#### Super Admin (Global)
- **Scope**: System-wide access across all tenants
- **Permissions**: Full system administration, tenant management
- **Use case**: Platform operators, system administrators

#### Tenant Admin
- **Scope**: Single tenant with full administrative access
- **Permissions**: User management, tenant configuration, billing
- **Use case**: Organization administrators, IT managers

#### Tenant Manager
- **Scope**: Single tenant with operational access
- **Permissions**: Document management, user onboarding, reporting
- **Use case**: Department managers, team leads

#### Security Admin
- **Scope**: Single tenant with security focus
- **Permissions**: Access control, audit logs, security policies
- **Use case**: Security officers, compliance managers

#### User Manager
- **Scope**: Single tenant with user management focus
- **Permissions**: User creation, role assignment, profile management
- **Use case**: HR managers, team administrators

#### User
- **Scope**: Single tenant with standard access
- **Permissions**: Document access, query submission, profile management
- **Use case**: Regular employees, knowledge workers

#### Guest
- **Scope**: Single tenant with limited access
- **Permissions**: Read-only access to public documents
- **Use case**: External contractors, temporary access

### Permission Matrix

| Resource | Super Admin | Tenant Admin | Tenant Manager | Security Admin | User Manager | User | Guest |
|----------|-------------|--------------|----------------|----------------|--------------|------|-------|
| **Tenant Management** |
| Create Tenant | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Update Tenant | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Delete Tenant | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **User Management** |
| Create User | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Update User | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Delete User | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Assign Roles | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Document Management** |
| Upload Document | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| View Document | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Update Document | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Delete Document | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Query & Search** |
| Submit Query | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| View Query History | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| **System Administration** |
| View Logs | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| System Configuration | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Billing & Usage | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Permission Implementation

### Policy-Based Access Control

#### Policy Structure
```python
# Example policy structure (pseudocode)
class Policy:
    def __init__(self, resource, action, conditions):
        self.resource = resource      # e.g., "document", "user", "tenant"
        self.action = action          # e.g., "create", "read", "update", "delete"
        self.conditions = conditions  # e.g., role requirements, ownership checks
        self.effects = effects        # "allow" or "deny"
```

#### Example Policies
```python
# Document access policy
document_read_policy = Policy(
    resource="document",
    action="read",
    conditions={
        "roles": ["user", "user_manager", "tenant_manager", "tenant_admin", "super_admin"],
        "ownership": "any",  # Can read any document in tenant
        "status": ["active", "archived"]
    }
)

# User management policy
user_create_policy = Policy(
    resource="user",
    action="create",
    conditions={
        "roles": ["user_manager", "tenant_manager", "tenant_admin", "super_admin"],
        "tenant_match": True,  # Must be in same tenant
        "role_limit": "user_manager"  # Cannot create users with higher roles
    }
)

# Tenant configuration policy
tenant_update_policy = Policy(
    resource="tenant",
    action="update",
    conditions={
        "roles": ["tenant_admin", "super_admin"],
        "ownership": True,  # Must own the tenant
        "scope": "own_tenant"  # Cannot modify other tenants
    }
)
```

### Permission Checking

#### Middleware Implementation
```python
# Permission checking middleware (pseudocode)
async def check_permissions(request, resource, action):
    user = request.user
    tenant_id = request.headers.get("X-Tenant-ID")
    
    # Get user's effective permissions
    permissions = await get_user_permissions(user.id, tenant_id)
    
    # Check if action is allowed
    if not permissions.can_perform(resource, action):
        raise PermissionDenied(f"Cannot {action} {resource}")
    
    # Apply additional conditions (ownership, scope, etc.)
    if not await validate_conditions(request, permissions.conditions):
        raise PermissionDenied("Additional conditions not met")
    
    return True
```

#### Service Layer Integration
```python
# Service method with permission check (pseudocode)
async def create_document(self, request, document_data):
    # Check permissions
    await check_permissions(request, "document", "create")
    
    # Validate tenant context
    tenant_id = request.headers.get("X-Tenant-ID")
    if not await self.tenant_service.is_active(tenant_id):
        raise TenantInactiveError(f"Tenant {tenant_id} is not active")
    
    # Check usage limits
    if not await self.tenant_service.check_document_limit(tenant_id):
        raise QuotaExceededError("Document limit exceeded")
    
    # Proceed with document creation
    document = await self.document_repository.create(
        tenant_id=tenant_id,
        user_id=request.user.id,
        **document_data
    )
    
    return document
```

## Tenant Isolation Implementation

### Database Level
```sql
-- Example tenant-scoped queries
-- All tables include tenant_id column
SELECT * FROM documents 
WHERE tenant_id = :tenant_id 
AND status = 'active';

-- Tenant-specific schemas (alternative approach)
SELECT * FROM tenant_acme_corp.documents 
WHERE status = 'active';
```

### Cache Level
```python
# Redis key patterns with tenant isolation
def get_cache_key(tenant_id, resource_type, resource_id):
    return f"tenant:{tenant_id}:{resource_type}:{resource_id}"

# Example keys
# tenant:acme_corp:document:doc_123
# tenant:acme_corp:user:user_456
# tenant:acme_corp:query:query_789
```

### Vector Database Level
```python
# Qdrant collection naming with tenant isolation
def get_collection_name(tenant_id):
    return f"documents_{tenant_id}"

# Example collections
# documents_acme_corp
# documents_tech_startup
# documents_consulting_firm
```

## Security Considerations

### Data Leakage Prevention
- **Strict tenant filtering**: All database queries must include tenant_id
- **Middleware validation**: Request-level tenant validation
- **Service layer checks**: Business logic tenant verification
- **Repository isolation**: Data access layer tenant enforcement

### Cross-Tenant Access Prevention
- **Role-based restrictions**: Users cannot access other tenants
- **API endpoint isolation**: Tenant context required for all operations
- **Audit logging**: All cross-tenant access attempts logged
- **Regular security reviews**: Periodic permission audits

### Compliance and Auditing
- **Access logs**: All permission checks logged with context
- **Change tracking**: Role and permission modifications tracked
- **Regular reviews**: Quarterly access control reviews
- **Incident response**: Security incident procedures for permission violations

## Implementation Guidelines

### Best Practices
1. **Principle of least privilege**: Grant minimum permissions necessary
2. **Role inheritance**: Use role hierarchies for permission management
3. **Regular audits**: Periodic review of user permissions and roles
4. **Documentation**: Clear documentation of all roles and permissions
5. **Testing**: Comprehensive testing of permission boundaries

### Common Pitfalls
1. **Missing tenant context**: Forgetting to include tenant_id in queries
2. **Overly permissive roles**: Granting unnecessary permissions
3. **Inconsistent enforcement**: Different layers using different permission logic
4. **Hard-coded permissions**: Embedding permission logic in business code
5. **Lack of testing**: Not testing permission edge cases

### Monitoring and Alerting
- **Permission failures**: Alert on repeated permission denials
- **Role changes**: Log all role modifications
- **Cross-tenant attempts**: Alert on potential security violations
- **Usage patterns**: Monitor for unusual permission usage
