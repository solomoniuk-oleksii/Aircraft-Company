from flask import render_template, url_for, request, redirect
from dbinit import app, db
from model import Department, District, ProductCat, ProductType, Product, ProductCatAttr, PersonnelCat, Personnel, PersonnelCatAttr, Brigade, TestingLab, Test, TestingEquipment, ProductWorkProcess


@app.route('/')
def index():
    cats = ProductCat.query.order_by(ProductCat.name).all()
    return render_template("index.html", categories=cats)

@app.route('/product_types', methods=['POST','GET'])
def product_types():
    cats = ProductCat.query.all()
    deps = Department.query.all()
    prod_types = ProductType.query.join(ProductCat, ProductCat.id == ProductType.cat_id)
    if request.method == 'POST':
        if request.form['category'] != '':
            category = request.form['category']
            prod_types = prod_types.filter(ProductType.cat_id == category)
        if request.form['department'] != '':
            department = request.form['department']
            prod_types = prod_types.join(Product, Product.type_id == ProductType.id, isouter=True).filter(Product.department_id == department)

        print(prod_types)
        return render_template("producttypes.html", prod_types=prod_types, cats=cats, deps=deps,  total=prod_types.count())
    else:
        print(prod_types)
        return render_template("producttypes.html", prod_types=prod_types, cats=cats, deps=deps,  total=prod_types.count())

@app.route('/products', methods=['POST','GET'])
def products():
    cats = ProductCat.query.all()
    deps = Department.query.all()
    distrs = District.query.all()
    labs = TestingLab.query.all()
    prods = Product.query.join(ProductType, Product.type_id == ProductType.id).join(Department,
            Product.department_id == Department.id).join(ProductCat, ProductType.cat_id == ProductCat.id).join(ProductCatAttr, ProductCatAttr.prod_id == Product.id, isouter=True).order_by(Product.id)
    if request.method == 'POST':
        cat_id = int(request.form['cat'])
        dep_id = int(request.form['dep'])
        beg_date = request.form.get('begDate')
        end_date = request.form.get('endDate')
        if cat_id == 0 and dep_id == 0:
            redirect("/products")
        else:
            if cat_id == 0:
                prods = prods.filter(Product.department_id == dep_id)
            elif dep_id == 0:
                prods = prods.filter(ProductCat.id == cat_id)
            else:
                prods = prods.filter(ProductCat.id == cat_id, Product.department_id == dep_id)

        if request.form['district'] != '' or request.form.get('assembling') == 'on':
            prods = prods.join(ProductWorkProcess, ProductWorkProcess.prod_id == Product.id)
        if request.form['district'] != '':
            district = request.form['district']
            #print(request.form['district'])
            prods = prods.filter(
            ProductWorkProcess.district_id == district)
        if request.form.get('assembling') == 'on':
            #print(request.form.get('assembling'))
            prods = prods.filter(
            ProductWorkProcess.finish_date == None)
            '''prods = Product.query.join(ProductType, Product.type_id == ProductType.id).join(Department,
            Product.department_id == Department.id).join(ProductCat, ProductType.cat_id == ProductCat.id).join(ProductCatAttr,
            ProductCatAttr.prod_id == Product.id, isouter=True).join(ProductWorkProcess, ProductWorkProcess.prod_id == Product.id).filter(
            ProductWorkProcess.finish_date == None)'''
            print(prods)
            return render_template("products.html", products=prods, cats=cats, deps=deps, distrs=distrs, labs=labs, total=prods.count())

        if beg_date != '':
            prods = prods.filter(Product.assembly_date >= beg_date)
        if end_date != '':
            prods = prods.filter(Product.assembly_date <= end_date)

        prods = prods.join(Test, Test.prod_id == Product.id, isouter=True)
        if request.form['testinglab'] != '':
            testinglab = request.form['testinglab']
            prods = prods.filter(Test.testing_lab_id == testinglab)

        if request.form.get('testBegDate') != '':
            test_beg_date = request.form.get('testBegDate')
            prods = prods.filter(Test.test_date >= test_beg_date)
        if request.form.get('testBegDate') != '':
            test_end_date = request.form.get('testEndDate')
            prods = prods.filter(Test.test_date <= test_end_date)

        print(prods)
        return render_template("products.html", products=prods, cats=cats, deps=deps, distrs=distrs, labs=labs, total=prods.count())
    else:
        print(prods)
        return render_template("products.html", products=prods, cats=cats, deps=deps, distrs=distrs, labs=labs, total=prods.count())


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if request.method == 'GET':

        if request.args.get('cats') is None:
            return redirect('/products')

        catid = int(request.args.get('cats'))
        types = ProductType.query.filter_by(cat_id=catid)
        deps = Department.query.all()
        return render_template("addproduct.html", types=types, deps=deps, cat=catid)
    else:
        name = request.form['name']
        status = request.form['status']
        type_id = request.form['types']
        dep_id = request.form['deps']
        date = request.form['date']
        if request.form['eng_pow'] != '':
            eng_pow = request.form['eng_pow']
        else:
            eng_pow = None
        if request.form['wind_min_speed'] != "":
            wind_min_speed = request.form['wind_min_speed']
        else:
            wind_min_speed = None
        if request.form['wind_max_speed'] != "":
            wind_max_speed = request.form['wind_max_speed']
        else:
            wind_max_speed = None
        if request.form['wingspan'] != "":
            wingspan = request.form['wingspan']
        else:
            wingspan = None
        if request.form['flight_speed'] != "":
            flight_speed = request.form['flight_speed']
        else:
            flight_speed = None
        if request.form['eng_num'] != "":
            eng_num = request.form['eng_num']
        else:
            eng_num = None
        if request.form['expl_pow'] != "":
            expl_pow = request.form['expl_pow']
        else:
            expl_pow = None
        product = Product(name=name, status=status, type_id=type_id, department_id=dep_id, assembly_date=date)
        '''product_cat_attr = ProductCatAttr(prod_id=int(Product.query.order_by(Product.id.desc()).first().id) + 1,
                                          engine_power=eng_pow, wind_min_speed=wind_min_speed,
                                          wind_max_speed=wind_max_speed, wingspan=wingspan, flight_speed=flight_speed,
                                          engine_num=eng_num, explosion_power=expl_pow)'''
        product_cat_attr = ProductCatAttr(engine_power=eng_pow, wind_min_speed=wind_min_speed,
                                          wind_max_speed=wind_max_speed, wingspan=wingspan, flight_speed=flight_speed,
                                          engine_num=eng_num, explosion_power=expl_pow)
        product.prod_cat_attr = product_cat_attr
        try:
            db.session.add(product)
            db.session.commit()
            db.session.add(product_cat_attr)
            db.session.commit()
            return redirect('/products')
        except:
            return "Error!"


@app.route('/personnel', methods=['POST', 'GET'])
def personnel():
    empls = Personnel.query.join(PersonnelCat, Personnel.cat_id == PersonnelCat.id).order_by(Personnel.id).join(
        Brigade, Brigade.id == Personnel.brigade_id, isouter=True)
    pcats = PersonnelCat.query.all()
    deps = Department.query.all()
    dists = District.query.all()
    tlabs = TestingLab.query.all()
    brigs = Brigade.query.all()
    if request.method == 'POST':
        #print(request.form.get('master'))
        if request.form['department'] != '':
            department = request.form['department']
            empls = empls.filter(Personnel.department_id == department)
        if request.form['district'] != '':
            district = request.form['district']
            empls = empls.filter(Brigade.district_id == district)
        if request.form['category'] != '':
            category = request.form['category']
            empls = empls.filter(Personnel.cat_id == category)
        if request.form.get('master') == 'on':
            empls = empls.filter(Personnel.master == 1).order_by(Personnel.id)
        print(empls)
        return render_template("personnel.html", empls=empls, cats=pcats, deps=deps, brigs=brigs, tlabs=tlabs, dists=dists, total=empls.count())
    else:
        print(empls)
        return render_template("personnel.html", empls=empls, cats=pcats, deps=deps, brigs=brigs, tlabs=tlabs, dists=dists, total=empls.count())

'''
@app.route('/addpersonnel', methods=['POST', 'GET'])
def addpersonnel():
    if request.method == 'GET':

        if request.args.get('cats') is None:
            return redirect('/products')

        catid = int(request.args.get('cats'))
        deps = Department.query.all()
        brigs = Brigade.query.all()
        tlabs = TestingLab.query.all()
        return render_template("addpersonnel.html", deps=deps, brigs=brigs, tlabs=tlabs, cat=catid)
    else:
        fullname = request.form['fullname']
        address = request.form['address']
        master = request.form['master']
        dep_id = request.form['department']
        brig_id = request.form['brigs']
        tlab_id = request.form['testing_lab']
        catid = request.form['catid']

        if request.form['engineer_class'] != '':
            engineer_class = request.form['engineer_class']
        else:
            engineer_class = None
        if request.form['attr2'] != '':
            attr2 = request.form['attr2']
        else:
            attr2 = None
        if request.form['attr3'] != '':
            attr3 = request.form['attr3']
        else:
            attr3 = None

        personnel = Personnel(fullname=fullname, cat_id=catid, address=address, master=master,
                              department_id=dep_id, brigade_id=brig_id, testing_lab_id=tlab_id)

        pers_cat_attr = PersonnelCatAttr(engineer_class=engineer_class, attr2=attr2, attr3=attr3)
        personnel.personnel_cat_attr = pers_cat_attr
        try:
            db.session.add(personnel)
            db.session.commit()
            db.session.add(pers_cat_attr)
            db.session.commit()
            return redirect('/personnel')
        except:
            return "Error!"
'''

@app.route('/district', methods=['POST', 'GET'])
def district():
    dists = District.query.join(Personnel, Personnel.id == District.chief_id).order_by(District.id)
    deps = Department.query.all()
    if request.method == 'POST':
        if request.form['department'] != '':
            department = request.form['department']
            dists = District.query.filter(District.department_id == department)
        else:
            dists = District.query.join(Personnel, Personnel.id == District.chief_id).order_by(District.id)

        print(dists)
        return render_template("district.html", dists=dists, deps=deps, total=dists.count())
    else:
        print(dists)
        return render_template("district.html", dists=dists, deps=deps, total=dists.count())


@app.route('/workprocess', methods=['POST', 'GET'])
def workprocess():
    works = ProductWorkProcess.query.join(Product, Product.id == ProductWorkProcess.prod_id).join(
            Brigade, Brigade.id == ProductWorkProcess.brigade_id).join(
            District, District.id == Brigade.district_id).order_by(ProductWorkProcess.id)
    prods = Product.query.all()
    if request.method == 'POST':
        if request.form['product'] != '':
            product = request.form['product']
            works = ProductWorkProcess.query.join(Product, Product.id == ProductWorkProcess.prod_id).join(
                Brigade, Brigade.id == ProductWorkProcess.brigade_id).join(
                District, District.id == Brigade.district_id).filter(ProductWorkProcess.prod_id==product).order_by(ProductWorkProcess.id)
        else:
            works = ProductWorkProcess.query.join(Product, Product.id == ProductWorkProcess.prod_id).join(
                Brigade, Brigade.id == ProductWorkProcess.brigade_id).join(
                District, District.id == Brigade.district_id).order_by(ProductWorkProcess.id)
        print(works)
        return render_template("workprocess.html", works=works, prods=prods, total=works.count())
    else:
        print(works)
        return render_template("workprocess.html", works=works, prods=prods, total=works.count())


@app.route('/brigade', methods=['POST', 'GET'])
def brigade():
    brigades = Brigade.query.join(Personnel, Personnel.id == Brigade.chief_id).join(
            District, District.id == Brigade.district_id)
    deps = Department.query.all()
    distrs = District.query.all()
    workers = Personnel.query.all()
    prods = Product.query.all()
    if request.method == 'POST':
        if request.form['department'] != '':
            department = request.form['department']
            brigades = brigades.filter(District.department_id == department)
        if request.form['district'] != '':
            district = request.form['district']
            brigades = brigades.filter(Brigade.district_id == district).distinct()
        if request.form['product'] != '':
            product = request.form['product']
            brigades = brigades.join(ProductWorkProcess, ProductWorkProcess.brigade_id == Brigade.id).filter(ProductWorkProcess.prod_id == product).distinct()
        print(brigades)
        return render_template("brigade.html", brigades=brigades, deps=deps, distrs=distrs, prods=prods, workers=workers, total=brigades.count())
    else:
        print(brigades)
        return render_template("brigade.html", brigades=brigades, deps=deps, distrs=distrs, prods=prods, workers=workers, total=brigades.count())


@app.route('/laboratory', methods=['POST', 'GET'])
def laboratory():
    labs = TestingLab.query.join(Test, Test.testing_lab_id == TestingLab.id, isouter=True)
    prods = Product.query.all()
    if request.method == 'POST':
        if request.form['product'] != '':
            product = request.form['product']
            labs = labs.filter(Test.prod_id == product)
        print(labs)
        return render_template("laboratory.html", labs=labs, prods=prods, total=labs.count())
    else:
        print(labs)
        return render_template("laboratory.html", labs=labs, prods=prods, total=labs.count())



@app.route('/tester', methods=['POST', 'GET'])
def tester():
    labs = TestingLab.query.all()
    prods = Product.query.all()
    cats = ProductCat.query.all()
    testers = Personnel.query.filter(Personnel.testing_lab_id != None)
    if request.method == 'POST':
        if request.form['product'] != '' or request.form['category'] != '' or request.form.get('testBegDate') != '' or request.form.get('testEndDate') != '' or request.form['testinglab'] != '':
            testers = testers.join(Test, Test.tester_id == Personnel.id)
        if request.form['product'] != '':
            product = request.form['product']
            testers = testers.filter(Test.prod_id == product)
        if request.form['category'] != '':
            category = request.form['category']
            testers = testers.join(Product, Product.id == Test.prod_id).join(
                ProductType, ProductType.id == Product.type_id).filter(ProductType.cat_id == category)
        if request.form['testinglab'] != '':
            testinglab = request.form['testinglab']
            testers = testers.filter(Test.testing_lab_id == testinglab)
        if request.form.get('testBegDate') != '':
            test_beg_date = request.form.get('testBegDate')
            testers = testers.filter(Test.test_date >= test_beg_date)
        if request.form.get('testEndDate') != '':
            test_end_date = request.form.get('testEndDate')
            testers = testers.filter(Test.test_date <= test_end_date)
        print(testers)
        return render_template("tester.html", labs=labs, prods=prods, cats=cats, testers=testers, total=testers.count())
    else:
        print(testers)
        return render_template("tester.html", labs=labs, prods=prods, cats=cats, testers=testers, total=testers.count())


@app.route('/testingequipment', methods=['POST', 'GET'])
def testingequipment():
    labs = TestingLab.query.all()
    prods = Product.query.all()
    cats = ProductCat.query.all()
    equips = TestingEquipment.query.join(Test, TestingEquipment.test, isouter=True)
    if request.method == 'POST':
        #if request.form['product'] != '' or request.form['category'] != '' or request.form.get('testBegDate') != '' or request.form.get('testEndDate') != '' or request.form['testinglab'] != '':
            #equips = TestingEquipment.query.join(Test, TestingEquipment.test)
        if request.form['product'] != '':
            product = request.form['product']
            equips = equips.filter(Test.prod_id == product)
        if request.form['category'] != '':
            category = request.form['category']
            equips = equips.join(Product, Product.id == Test.prod_id).join( #        outerjoin ???
                ProductType, ProductType.id == Product.type_id).filter(ProductType.cat_id == category)
        if request.form['testinglab'] != '':
            testinglab = request.form['testinglab']
            equips = equips.filter(Test.testing_lab_id == testinglab)
        if request.form.get('testBegDate') != '':
            test_beg_date = request.form.get('testBegDate')
            equips = equips.filter(Test.test_date >= test_beg_date)
        if request.form.get('testEndDate') != '':
            test_end_date = request.form.get('testEndDate')
            equips = equips.filter(Test.test_date <= test_end_date)
        print(equips)
        return render_template("testingequipment.html", labs=labs, prods=prods, cats=cats, equips=equips,  total=equips.count())
    else:
        print(equips)
        return render_template("testingequipment.html", labs=labs, prods=prods, cats=cats, equips=equips,  total=equips.count())


if __name__ == "__main__":
    app.run(debug=True)
