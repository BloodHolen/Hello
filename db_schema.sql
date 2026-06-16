BEGIN;
--
-- Create model Category
--
CREATE TABLE "main_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE);
--
-- Create model Manufacturer
--
CREATE TABLE "main_manufacturer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE);
--
-- Create model PickupPoint
--
CREATE TABLE "main_pickuppoint" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address" varchar(500) NOT NULL UNIQUE);
--
-- Create model Supplier
--
CREATE TABLE "main_supplier" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE);
--
-- Create model Unit
--
CREATE TABLE "main_unit" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE);
--
-- Create model User
--
CREATE TABLE "main_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "role" varchar(20) NOT NULL, "patronymic" varchar(150) NOT NULL);
CREATE TABLE "main_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "main_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "main_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "main_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Order
--
CREATE TABLE "main_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "code" varchar(50) NOT NULL UNIQUE, "order_number" integer NOT NULL, "order_date" date NOT NULL, "delivery_date" date NOT NULL, "status" varchar(20) NOT NULL, "client_id" bigint NOT NULL REFERENCES "main_user" ("id") DEFERRABLE INITIALLY DEFERRED, "pickup_point_id" bigint NOT NULL REFERENCES "main_pickuppoint" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Product
--
CREATE TABLE "main_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "article" varchar(50) NOT NULL UNIQUE, "name" varchar(500) NOT NULL, "price" decimal NOT NULL, "discount" integer unsigned NOT NULL CHECK ("discount" >= 0), "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "description" text NOT NULL, "photo" varchar(100) NULL, "category_id" bigint NOT NULL REFERENCES "main_category" ("id") DEFERRABLE INITIALLY DEFERRED, "manufacturer_id" bigint NOT NULL REFERENCES "main_manufacturer" ("id") DEFERRABLE INITIALLY DEFERRED, "supplier_id" bigint NOT NULL REFERENCES "main_supplier" ("id") DEFERRABLE INITIALLY DEFERRED, "unit_id" bigint NOT NULL REFERENCES "main_unit" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model OrderItem
--
CREATE TABLE "main_orderitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "order_id" bigint NOT NULL REFERENCES "main_order" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "main_product" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "main_user_groups_user_id_group_id_ae195797_uniq" ON "main_user_groups" ("user_id", "group_id");
CREATE INDEX "main_user_groups_user_id_df502602" ON "main_user_groups" ("user_id");
CREATE INDEX "main_user_groups_group_id_a337ba62" ON "main_user_groups" ("group_id");
CREATE UNIQUE INDEX "main_user_user_permissions_user_id_permission_id_96b9fadf_uniq" ON "main_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "main_user_user_permissions_user_id_451ce57f" ON "main_user_user_permissions" ("user_id");
CREATE INDEX "main_user_user_permissions_permission_id_cd2b56a3" ON "main_user_user_permissions" ("permission_id");
CREATE INDEX "main_order_client_id_e3685c50" ON "main_order" ("client_id");
CREATE INDEX "main_order_pickup_point_id_60fd3292" ON "main_order" ("pickup_point_id");
CREATE INDEX "main_product_category_id_c0d90f41" ON "main_product" ("category_id");
CREATE INDEX "main_product_manufacturer_id_0da06053" ON "main_product" ("manufacturer_id");
CREATE INDEX "main_product_supplier_id_0d5f19b5" ON "main_product" ("supplier_id");
CREATE INDEX "main_product_unit_id_76c71e64" ON "main_product" ("unit_id");
CREATE INDEX "main_orderitem_order_id_72ea9725" ON "main_orderitem" ("order_id");
CREATE INDEX "main_orderitem_product_id_b90dba64" ON "main_orderitem" ("product_id");
COMMIT;
