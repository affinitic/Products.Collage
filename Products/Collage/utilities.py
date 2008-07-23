import re

isNumber = re.compile(r"^\d+$")

def findFirstAvailableInteger(ids):
    i = 1
    while True:
        if str(i) not in ids:
            return i
        i += 1

def generateNewId(container):
    parent_contents = container.objectValues()
    contentIDs = map(lambda x: x.getId(), parent_contents)
    numericalIDs = filter(isNumber.match, contentIDs)
    return str(findFirstAvailableInteger(numericalIDs))


def faketranslate(text, default=""):
    """A fake translator to be used in AT schemas as i18ndude marker like this
    from Products.Collage.utils import faketranslate as _
    ...
    widget = FooWidget('foo', label_msgid=_('label_foo', default="Foo"), ...)
    """
    return text
