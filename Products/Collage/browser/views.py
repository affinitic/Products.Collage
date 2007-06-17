from Products.Five.browser import BrowserView

class SimpleView(BrowserView):
    def test(self):
        return lambda a, b, c: a and b or c

class RowView(SimpleView):
    def getColumnBatches(self, bsize=3):
        columns = self.context.getFolderContents()
        if not columns:
            return []

        # calculate number of batches
        count = (len(columns)-1)/3+1
        
        batches = []
        for c in range(count):
            batch = []
            for i in range(bsize):
                index = c*bsize+i

                # pad with null-columns
                column = None

                if index < len(columns):
                    column = columns[index]

                # do not pad first row
                if column or c > 0:
                    batch += [column]
                
            batches += [batch]
        
        return batches

class StandardRowView(RowView):
    title = u'Automatic'

class StandardDocumentView(SimpleView):
    title = u'Standard'

class FeaturedDocumentView(StandardDocumentView):
    title = u'Featured'

