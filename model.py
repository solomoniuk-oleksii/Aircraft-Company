from dbinit import db


department_laboratory = db.Table('department_laboratory',
    db.Column('department_id', db.Integer, db.ForeignKey('department.id')),
    db.Column('testing_lab_id', db.Integer, db.ForeignKey('testing_lab.id'))
)


class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    districts = db.relationship('District', backref='department')
    products = db.relationship('Product', backref='department')
    personnels = db.relationship('Personnel', backref='department')

    testing_lab = db.relationship('TestingLab', secondary=department_laboratory, backref=db.backref('dep'))

    def __repr__(self):
        return '<Department %r>' % self.id


class District(db.Model):
    __tablename__ = 'district'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    chief_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)

    brigades = db.relationship('Brigade', backref='district')
    product_work_process = db.relationship('ProductWorkProcess', backref='district')

    def __repr__(self):
        return '<District %r>' % self.id


class ProductCat(db.Model):
    __tablename__ = 'product_cat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    types = db.relationship('ProductType', backref='cat')

    def __repr__(self):
        return '<ProductCat %r>' % self.id


class ProductType(db.Model):
    __tablename__ = 'product_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('product_cat.id'), nullable=False)

    products = db.relationship('Product', backref='type')

    def __repr__(self):
        return '<ProductTypes %r>' % self.id


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=True)
    type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    assembly_date = db.Column(db.Date, nullable=True)

    prod_cat_attr = db.relationship('ProductCatAttr', uselist=False, backref='product')
    #tests = db.relationship('Test', backref='product')
    product_work_process = db.relationship('ProductWorkProcess', backref='prod')

    def __repr__(self):
        return '<Product %r>' % self.id


class ProductCatAttr(db.Model):
    __tablename__ = 'product_cat_attr'
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    engine_power = db.Column(db.String(30), nullable=True)
    wind_min_speed = db.Column(db.String(30), nullable=True)
    wind_max_speed = db.Column(db.String(30), nullable=True)
    wingspan = db.Column(db.String(30), nullable=True)
    flight_speed = db.Column(db.String(30), nullable=True)
    engine_num = db.Column(db.String(30), nullable=True)
    explosion_power = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<ProductCatAttr %r>' % self.id


class PersonnelCat(db.Model):
    __tablename__ = 'personnel_cat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    personnels = db.relationship('Personnel', backref='personnel_cat')


class Personnel(db.Model):
    __tablename__ = 'personnel'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('personnel_cat.id'), nullable=False)
    address = db.Column(db.String(30), nullable=True)
    master = db.Column(db.Integer, nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    brigade_id = db.Column(db.Integer, nullable=True)
    testing_lab_id = db.Column(db.Integer, db.ForeignKey('testing_lab.id'), nullable=True)

    districts = db.relationship('District', backref='chief')
    personnel_cat_attr = db.relationship('PersonnelCatAttr', uselist=False, backref='personnel')
    #tests = db.relationship('Test', backref='personnel')

    def __repr__(self):
        return '<Personnel %r>' % self.id


class PersonnelCatAttr(db.Model):
    __tablename__ = 'personnel_cat_attr'
    id = db.Column(db.Integer, primary_key=True)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'))
    engineer_class = db.Column(db.String(30), nullable=True)
    welder_qualification = db.Column(db.String(30), nullable=True)
    turner_work_exp = db.Column(db.String(30), nullable=True)


class Brigade(db.Model):
    __tablename__ = 'brigade'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    chief_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)

    chief = db.relationship('Personnel', backref='brigade')
    product_work_process = db.relationship('ProductWorkProcess', backref='brigade')

    def __repr__(self):
        return '<Brigade %r>' % self.id


class TestingLab(db.Model):
    __tablename__ = 'testing_lab'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    #personnels = db.relationship('Personnel', backref='testing_lab')
    #tests = db.relationship('Personnel', backref='testing_lab')


    def __repr__(self):
        return '<TestingLab %r>' % self.id


testing_equipment_usage = db.Table('testing_equipment_usage',
    db.Column('test_id', db.Integer, db.ForeignKey('test.id')),
    db.Column('testing_equipment_id', db.Integer, db.ForeignKey('testing_equipment.id'))
)


class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    tester_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    testing_lab_id = db.Column(db.Integer, db.ForeignKey('testing_lab.id'), nullable=False)
    test_date = db.Column(db.Date, nullable=True)

    equipment = db.relationship('TestingEquipment', secondary=testing_equipment_usage, backref=db.backref('test'))

    #testing_equipment = db.relationship('TestingEquipment', backref='test')

    def __repr__(self):
        return '<Test %r>' % self.id


class TestingEquipment(db.Model):
    __tablename__ = 'testing_equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<TestingEquipment %r>' % self.id


class ProductWorkProcess(db.Model):
    __tablename__ = 'product_work_process'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    status = db.Column(db.String(30), nullable=True)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    brigade_id = db.Column(db.Integer, db.ForeignKey('brigade.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    finish_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return '<ProductWorkProcess %r>' % self.id




'''
class TechnicalStaffCat(db.Model):
    __tablename__ = 'technicalstaffcat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<TechnicalStaffCat %r>' % self.id


class TechnicalStaff(db.Model):
    __tablename__ = 'technicalstaff'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('technicalstaffcat.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<TechnicalStaff %r>' % self.id


class WorkmanCat(db.Model):
    __tablename__ = 'workmancat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<WorkmanCat %r>' % self.id


class Workman(db.Model):
    __tablename__ = 'workman'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('workmancat.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    qualification = db.Column(db.String(255), nullable=False)
    brigade_id = db.Column(db.Integer, db.ForeignKey('brigade.id'), nullable=True)

    def __repr__(self):
        return '<Workman %r>' % self.id
'''



'''
class Tester(db.Model):
    __tablename__ = 'tester'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    testing_lab_id = db.Column(db.Integer, db.ForeignKey('testinglab.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Tester %r>' % self.id
'''