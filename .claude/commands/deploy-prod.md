# Production Deployment Command

Execute full WorkwearWatch production deployment with comprehensive quality gates and zero-downtime deployment.

## Usage
Type `/deploy-prod` to initiate complete production deployment pipeline.

## Actions Performed
1. **Quality Gates**: Code quality, security, test coverage validation
2. **Database Backup**: SQLite backup before deployment
3. **API Deployment**: Render production deployment
4. **Dashboard Deployment**: Netlify production build and deploy
5. **Health Validation**: Post-deployment system verification

## Command Execution
```bash
echo "🚀 WorkwearWatch Production Deployment"
echo "======================================"

# Pre-deployment quality checks
echo "🔍 Running quality gates..."
./scripts/quality_check.sh

# Database backup
echo "💾 Backing up database..."
./scripts/db_backup.sh

# Deploy API to Render
echo "🌐 Deploying API to Render..."
git push origin master  # Render auto-deploys from GitHub

# Build and deploy dashboard to Netlify
echo "📱 Deploying Dashboard to Netlify..."
cd dashboard
npm run build
netlify deploy --prod --dir=out
cd ..

# Post-deployment validation
echo "✅ Validating deployment..."
./scripts/health_monitor.py

# Final system check
echo "📊 Final health check..."
curl -f https://product-prices-api.onrender.com/ping || echo "⚠️ API health check failed"
curl -f https://your-dashboard.netlify.app || echo "⚠️ Dashboard health check failed"

echo "🎉 Deployment complete!"
```

## Quality Gates (Must Pass)
- ✅ Ruff linting and formatting
- ✅ MyPy type checking (strict mode)
- ✅ Bandit security scanning
- ✅ pytest with 80%+ coverage
- ✅ Database integrity validation

## Expected Output
- Pre-flight checklist results
- Render deployment status
- Netlify build and deployment logs
- Post-deployment health metrics
- Performance validation (API response times)

## Rollback Procedure
If deployment fails:
1. Restore database from backup
2. Revert to previous Render deployment
3. Rollback Netlify to last known good build
4. Execute emergency health check

## Context
Maintains production-ready system serving sophisticated streetwear enthusiasts with 95% reliability target.
