# Alfresco Add-ons

This directory contains third-party add-ons and extensions for the Alfresco deployment.

## Installed Add-ons

### Geo Views 2.5.0
- **File**: `geo-views-2.5.0.jar`
- **Source**: https://github.com/share-extras/geo-views
- **Description**: Provides geographic visualization capabilities for documents
- **Features**:
  - Geographic document views in document library
  - Map-based content visualization
  - Geotagged content support
  - Geographic dashlets for sites
  - Document location details view

## Installation

Add-ons in this directory are automatically mounted into the Alfresco containers via Docker Compose volume mounts. No manual installation is required for new deployments.

## Adding New Add-ons

1. Download the JAR file to this directory
2. Update the relevant Docker Compose file to mount the JAR
3. Restart the Alfresco services
4. Commit the JAR file to Git (allowed by .gitignore exception)