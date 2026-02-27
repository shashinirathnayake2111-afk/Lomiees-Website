from app import app, db, SizeChart

def test_recommendation(gender, height, weight):
    # Mimic the logic in app.py
    with app.app_context():
        potential_sizes = SizeChart.query.filter_by(gender=gender).all()
        best_size = None
        for s in potential_sizes:
            if s.min_height <= height <= s.max_height and s.min_weight <= weight <= s.max_weight:
                best_size = s.size
                break
        
        if not best_size and potential_sizes:
            min_dist = float('inf')
            for s in potential_sizes:
                h_diff = min(abs(height - s.min_height), abs(height - s.max_height)) if not (s.min_height <= height <= s.max_height) else 0
                w_diff = min(abs(weight - s.min_weight), abs(weight - s.max_weight)) if not (s.min_weight <= weight <= s.max_weight) else 0
                dist = h_diff + (w_diff * 2)
                if dist < min_dist:
                    min_dist = dist
                    best_size = s.size
        return best_size

if __name__ == "__main__":
    test_cases = [
        ('Men', 170, 70, 'M'),
        ('Women', 160, 50, 'S'),
        ('Kids', 120, 26, '6-8Y'),
        ('Men', 190, 95, 'XL'), 
    ]
    
    for gender, h, w, expected in test_cases:
        result = test_recommendation(gender, h, w)
        print(f"Test {gender}, {h}cm, {w}kg: Expected {expected}, Got {result}")
