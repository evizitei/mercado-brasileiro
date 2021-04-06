# Generated by Django 3.1.6 on 2021-04-02 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mercado_brasileiro', '0023_auto_20210402_1837'),
    ]

    operations = [
        migrations.RunSQL(
        """
        CREATE OR REPLACE FUNCTION update_inventory_value(sid mercado_brasileiro_seller.seller_uuid%TYPE)
        RETURNS void
        LANGUAGE plpgsql
        AS $$
        BEGIN
          UPDATE mercado_brasileiro_seller
            SET inventory_value = COALESCE(
                (
                SELECT SUM(line_items.line_item_value)
                FROM (
                    SELECT inv.wholesale_unit_price * inv.count AS line_item_value
                    FROM mercado_brasileiro_inventoryitem inv
                    WHERE inv.seller_uuid = sid
                      AND inv.owned
                ) AS line_items
                ),
                0.0
            )
            WHERE mercado_brasileiro_seller.seller_uuid = sid;
        END;
        $$;
        """
        ),
        migrations.RunSQL(
        """
        CREATE OR REPLACE FUNCTION update_inventory_event() RETURNS trigger AS $update_inventory_event$
        BEGIN
            if TG_op = 'UPDATE' then
              PERFORM update_inventory_value(OLD.seller_uuid);
              PERFORM update_inventory_value(NEW.seller_uuid);
            elsif TG_op = 'INSERT' then
              PERFORM update_inventory_value(NEW.seller_uuid);
            elsif TG_op = 'DELETE' then
              PERFORM update_inventory_value(OLD.seller_uuid);
            end if;
            RETURN NEW;
        END;
        $update_inventory_event$ LANGUAGE plpgsql;
        """
        ),
        migrations.RunSQL(
        """
        CREATE TRIGGER seller_inventory_sync
        AFTER INSERT OR UPDATE OR DELETE
        ON mercado_brasileiro_inventoryitem
        FOR EACH ROW
        EXECUTE PROCEDURE update_inventory_event();
        """
        ),
    ]