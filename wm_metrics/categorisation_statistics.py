# -*- coding: utf-8 -*-

"""Categorisation statistics."""


def make_categorisation_report(all_categories, categories_count_per_file):
    """Compute statistics on the categorisation.

    Return a text report on the categorisation.

    """
    numpy_available = True
    try:
        import numpy
    except ImportError:
        numpy_available = False
    text = list()
    text.append("= Categoriation statistics =")
    text.append("== Per category ==")
    text.append("The collection has {0:d} categories, {1:d} distinct ones".format(sum(all_categories.values()),
                                                                                  len(all_categories)))
    try:
        text.append("The most used category is on {0:d} files".format(max(all_categories.values())))
        text.append("The less used on {0:d} files".format(min(all_categories.values())))
    except ValueError:
        pass
    if numpy_available:
        text.append("On average, a category is used {0:.1f} times (mean)".format(numpy.mean(all_categories.values())))
        text.append("The median is: {0:.1f}".format(numpy.median(all_categories.values())))
    text.append("The 10 most used categories are:")
    text.append(" - ".join([unicode(x[0]) + ' - ' + unicode(x[1])
                            for x in all_categories.most_common(10)]))
    text.append("The 10 less used categories are:")
    text.append(" - ".join([unicode(x[0]) + ' - ' + unicode(x[1])
                            for x in all_categories.most_common()[-10:]]))

    text.append("== Per file ==")
    text.append("The most categorized file has {0:d} categories".format(max(categories_count_per_file.values())))
    text.append("The less categorized file has {0:d} categories".format(min(categories_count_per_file.values())))
    text.append("We have {0:d} uncategorized files".format(len([x for x in categories_count_per_file
                                                           if categories_count_per_file[x] is 0])))
    more_than_two = len([x for x in categories_count_per_file
                         if categories_count_per_file[x] >= 2])
    more_than_two_percentage = float(more_than_two) / len(categories_count_per_file) * 100
    text.append("We have {0:d} files with two categories or more, which makes {1:.1f}%".format(more_than_two,
                                                                                               more_than_two_percentage))
    if numpy_available:
        text.append("On average, a file has {0:.1f} categories (mean)".format(numpy.mean(categories_count_per_file.values())))
        text.append("The median is: {0:.1f}".format(numpy.median(categories_count_per_file.values())))
    return '\n'.join(text)
