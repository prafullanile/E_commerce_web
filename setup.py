from market import app, db, Item

with app.app_context():
    item1 = Item(name="iPhone 15", price=1200, barcode="123456789999", description="Latest iPhone with USB-C port")
    item2 = Item(name="Dell XPS 15", price=1800, barcode="987654321111", description="Slim high-performance laptop")


    db.session.add_all([item1, item2 ])
    db.session.commit()
