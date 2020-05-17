class VMWriter():
    def __init__(self, output):
        self._f = open(output, "w")
        return

    def write_push(self, segment, index):
        s = "push {} {}\n".format(segment, str(index))
        self._f.write(s)
        return

    def write_pop(self, segment, index):
        s = "pop {} {}\n".format(segment, str(index))
        self._f.write(s)
        return

    def write_arithmetic(self, command):
        self._f.write(command + "\n")
        return

    def write_label(self, label):
        s = "label {}\n".format(label)
        self._f.write(s)
        return

    def write_goto(self, label):
        s = "goto {}\n".format(label)
        self._f.write(s)
        return

    def write_if(self, label):
        s = "if-goto {}\n".format(label)
        self._f.write(s)
        return

    def write_call(self, name, num_args):
        s = "call {} {}\n".format(name, str(num_args))
        self._f.write(s)
        return

    def write_function(self, name, num_locals):
        s = "function {} {}\n".format(name, str(num_locals))
        self._f.write(s)
        return

    def write_return(self):
        self._f.write("return\n")
        return

    def close(self):
        self._f.close()
        return
