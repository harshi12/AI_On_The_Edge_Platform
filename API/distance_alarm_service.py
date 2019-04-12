class DistanceAlarmService(Service):
    def __init__(self, emergency_start, emergency_end, critical_start, critical_end,
                 all_fine_start, all_fine_end):
        self.em_start = emergency_start
        self.em_end = emergency_end
        self.cr_start = critical_start
        self.cr_end = critical_end
        self.fine_start = all_fine_start
        self.fine_end = all_fine_end

if __name__ == "__main__":
    
