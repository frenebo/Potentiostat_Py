
# def save_calibration()
class PotstatCalibrationSettings:
    def __init__(self, V_offset_pos: float, V_offset_neg: float):
        self.V_offset_pos = V_offset_pos
        self.V_offset_neg = V_offset_neg
    
    