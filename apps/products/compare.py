# apps/products/compare.py

class CompareProduct:
    def __init__(self, request):
        self.session = request.session
        compare = self.session.get('compare_product')
        
        if not compare:
            compare = self.session['compare_product'] = []
        
        self.compare_product = compare
        self.count = len(self.compare_product)
    
    def add_to_compare_product(self, product_id):
        """افزودن محصول به لیست مقایسه"""
        try:
            product_id = int(product_id)
        except:
            return False
            
        if product_id not in self.compare_product:
            if len(self.compare_product) >= 4:  # حداکثر 4 محصول
                return False
            self.compare_product.append(product_id)
            self.count = len(self.compare_product)
            self.save()
            return True
        return False
    
    def delete_form_compare_product(self, product_id):
        """حذف محصول از لیست مقایسه"""
        try:
            product_id = int(product_id)
        except:
            return False
            
        if product_id in self.compare_product:
            self.compare_product.remove(product_id)
            self.count = len(self.compare_product)
            self.save()
            return True
        return False
    
    def clear_compare_product(self):
        """خالی کردن لیست مقایسه"""
        self.compare_product = []
        self.count = 0
        self.save()
    
    def save(self):
        """ذخیره تغییرات در session"""
        self.session['compare_product'] = self.compare_product
        self.session.modified = True