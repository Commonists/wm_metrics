"""Representation of a period of time."""


class Period(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return "%s-%s" % (self.start, self.end)

    def __eq__(self, other):
        return ((other.start == self.start) and
                (other.end == self.end))
