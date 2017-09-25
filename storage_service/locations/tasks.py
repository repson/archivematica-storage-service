from __future__ import absolute_import

from celery import shared_task

from .models import Package


@shared_task
def replicate_package(package_uuid, replicator_location_uuid):
    """Replicates ``Package`` with UUID ``package_uuid`` to the
    replicator-purposed location with UUID ``replicator_location_uuid``.
    Creates a new ``Package`` model for it (which references the parent package
    in its ``replicated_package`` attribute)
    """
    replicandum_package = Package.objects.get(uuid=package_uuid)
    replicandum_package.replicate(replicator_location_uuid)


"""
CREATE TABLE "locations_package" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "uuid" varchar(36) NOT NULL UNIQUE,
    "current_path" text NOT NULL,
    "pointer_file_path" text NULL,
    "size" integer NOT NULL,
    "package_type" varchar(8) NOT NULL,
    "status" varchar(8) NOT NULL,
    "current_location_id" varchar(36) NOT NULL REFERENCES "locations_location" ("uuid"),
    "origin_pipeline_id" varchar(36) NULL REFERENCES "locations_pipeline" ("uuid"),
    "pointer_file_location_id" varchar(36) NULL REFERENCES "locations_location" ("uuid"),
    "misc_attributes" text NULL,
    "description" varchar(256) NULL,
    "replicated_package_id" varchar(36) NULL REFERENCES "locations_package" ("uuid"));


CREATE INDEX "locations_package_4c64ef65" ON "locations_package" ("current_location_id");
CREATE INDEX "locations_package_c621dfd4" ON "locations_package" ("origin_pipeline_id");
CREATE INDEX "locations_package_66655d4d" ON "locations_package" ("pointer_file_location_id");
CREATE INDEX "locations_package_505381cb" ON "locations_package" ("replicated_package_id");
"""
