class VMWriter():
    def __init__(self, output):
        self._f = open(output, "w")
        return

    def write_push(self, segment, index):
        return

    def write_pop(self, segment, index):
        return

    def write_arithmetic(self, command):
        return

    def write_label(self, label):
        return

    def write_goto(self, label):
        return

    def write_if(self, label):
        return

    def write_call(self, name, num_args):
        return

    def write_function(self, name, num_locals):
        s = "function {} {}\n".format(name, str(num_locals))
        self._f.write(s)
        return

    def write_return(self):
        return

    def close(self):
        self._f.close()
        return
