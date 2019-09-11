

# filename = './b_lovely_landscapes'
# filename = './c_memorable_moments'
# filename = './e_shiny_selfies'
filename = './d_pet_pictures'


class Photo:
    def __init__(self, orientation, tags, index,tagCount):
        self.orientation = orientation;
        self.tags = tags
        self.index = index
        self.tagCount= tagCount
        self.otherIndex = None
    def toString(self):
        return "{} {} {} {}".format(self.index,self.tagCount,self.tags,self.orientation)

def similarity(slide1_tags, slide2_tags):
    min_list = slide1_tags.tags
    max_list = slide2_tags.tags
    if (slide1_tags.tagCount) > (slide2_tags.tagCount):
        min_list = slide2_tags.tags
        max_list = slide1_tags.tags

    common_list_len = 0
    for tag in max_list:
        if tag in min_list:
            common_list_len += 1

    ans =  (common_list_len/len(min_list)) * 100
    # print("{} {} {}".format(ans, slide1_tags.tags, slide2_tags.tags))
    return ans

with open(filename+'.txt') as f:
    lines = f.read().splitlines()
    N = int(lines[0])
    photoList = list()

    previousVertical = None
    for i in range(1, N+1 ):
        explode = (lines[i].split(" "))
        O, tagCount = explode[0], explode[1]
        tags = explode[-int(tagCount):]
        photo = Photo(orientation=O, tags=tags, index=(i-1), tagCount=int(tagCount))
        if(photo.orientation=="H"):
            photoList.append(photo)
        else:
            if(previousVertical!= None):
                photo.otherIndex = previousVertical.index
                photo.tags = list(set( photo.tags+previousVertical.tags))
                photoList.append(photo)
                previousVertical = None;
            else:
                previousVertical = photo;



    photoList.sort(key=lambda x: x.tagCount, reverse=True)


    j = 0
    slideCount = len(photoList)
    while(j< slideCount-1 and j < slideCount):
        photo = photoList[j]
        k = j
        bestDistance = 50
        bestIndex = k+1
        if j%1000 ==0:
            print(j)
        counter = 0
        while(counter < 100 and k+1< slideCount and photoList[k+1].tagCount == photoList[j+1].tagCount  ):
            k+=1
            counter+=1

            currentSimilarity = similarity(photo, photoList[k]);
            if (currentSimilarity == 50):
                break
            if(abs(currentSimilarity - 50) < abs(bestDistance)):
                bestDistance = currentSimilarity -50
                bestIndex = k
        photoList[j+1], photoList[bestIndex] = photoList[bestIndex], photoList[j+1]
        j+=1

    res = ""
    res += str(slideCount)


    # print(slideCount)
    for photo in photoList:
        print(photo.index)
        if(photo.otherIndex !=None):
            res+='\n'+str(photo.otherIndex)+' '+str(photo.index)
        else:
            res+='\n'+str(photo.index)
    with open(filename+"-out.txt", "w") as text_file:
        text_file.write(res)