"""Simple NLP utility for parsing voice commands"""
import re

class VoiceCommandParser:
    """Parse voice commands to extract product details"""
    
    @staticmethod
    def parse_add_product(text):
        """
        Parse: "add product [name] price [price] quantity [quantity]"
        Or: "add product [name] price [price]"
        Returns: {product_name, price, quantity} or None if invalid
        """
        text = text.lower().strip()
        
        # Extract product name (between "add product" and "price")
        name_match = re.search(r'add\s+product\s+(.+?)\s+price', text)
        product_name = name_match.group(1).strip() if name_match else None
        
        # Extract price (number after "price")
        price_match = re.search(r'price\s+([\d.]+)', text)
        price = float(price_match.group(1)) if price_match else None
        
        # Extract quantity (number after "quantity") - optional, default to 1
        quantity_match = re.search(r'quantity\s+(\d+)', text)
        quantity = int(quantity_match.group(1)) if quantity_match else 1
        
        if product_name and price and price > 0:
            return {
                'product_name': product_name,
                'price': price,
                'quantity': quantity
            }
        return None
    
    @staticmethod
    def parse_check_stock(text):
        """Parse: "check stock" command"""
        return 'check stock' in text.lower()
    
    @staticmethod
    def parse_generate_report(text):
        """Parse: "generate report" command"""
        return 'generate report' in text.lower()
    
    @staticmethod
    def parse_show_statistics(text):
        """Parse: "show statistics" command"""
        return 'show statistics' in text.lower()
    
    @staticmethod
    def parse_complete_sale(text):
        """Parse: "complete sale" command"""
        return 'complete sale' in text.lower()
    
    @staticmethod
    def parse_clear_cart(text):
        """Parse: "clear cart" command"""
        return 'clear cart' in text.lower()
    
    @staticmethod
    def parse_list_products(text):
        """Parse: "show all products" or "list products" command"""
        text = text.lower()
        return 'show all products' in text or 'list products' in text or 'all products' in text
    
    @staticmethod
    def parse_product_details(text):
        """
        Parse: "product [name]" or "details [name]" command
        Returns: product_name or None
        """
        text = text.lower().strip()
        
        # Extract product name after "product" or "details"
        match = re.search(r'(?:product|details)\s+(.+?)(?:\s+|$)', text)
        if match:
            return match.group(1).strip()
        return None
    
    @staticmethod
    def parse_low_stock_alert(text):
        """Parse: "low stock" or "low stock products" command"""
        text = text.lower()
        return 'low stock' in text
    
    @staticmethod
    def parse_update_product(text):
        """
        Parse: "update product [name] price [price]" or "update product [name] quantity [quantity]"
        Returns: {product_name, price, quantity} or None if invalid
        """
        text = text.lower().strip()
        
        if 'update product' not in text:
            return None
        
        # Extract product name (between "update product" and next keyword)
        name_match = re.search(r'update\s+product\s+(.+?)(?:\s+(?:price|quantity)|$)', text)
        product_name = name_match.group(1).strip() if name_match else None
        
        # Extract price if present
        price_match = re.search(r'price\s+([\d.]+)', text)
        price = float(price_match.group(1)) if price_match else None
        
        # Extract quantity if present
        quantity_match = re.search(r'quantity\s+(\d+)', text)
        quantity = int(quantity_match.group(1)) if quantity_match else None
        
        if product_name and (price or quantity):
            return {
                'product_name': product_name,
                'price': price,
                'quantity': quantity
            }
        return None
