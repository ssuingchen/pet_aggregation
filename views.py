from django.shortcuts import render, redirect, get_object_or_404
import matplotlib.pyplot as plt
import io
import urllib, base64
import numpy as np
from django.views import View
from pets.models import Pet
from collections import defaultdict
from pets.utils import dump_queries
from django.db.models import Q

class MainView(View):
    def get(self, request):
        # pet_list = Pet.objects.all()

        strval =  request.GET.get("search", False)
        if strval :
            query = Q(breed__breed__icontains=strval)
            query.add(Q(color__color__icontains=strval), Q.OR)
            query.add(Q(age__age__icontains=strval), Q.OR)
            objects = Pet.objects.filter(query).select_related()[:10]
        else :
            objects = Pet.objects.all()[:10]

        # create a plot of number of each species
        species_list_id = [6,7,8,9,10]
        species_list = ["Dog", "other", "Cat", "Bird", "Rabbit"]
        dog = []
        other = []
        cat = []
        bird = []
        rabbit = []
        for obj in objects:
            if obj.species.id == 6:
                dog.append(1)
            elif obj.species.id == 7:
                other.append(1)
            elif obj.species.id == 8:
                cat.append(1)
            elif obj.species.id == 9:
                bird.append(1)
            elif obj.species.id == 10:
                rabbit.append(1)

        species_count = [len(dog), len(other), len(cat), len(bird), len(rabbit)]

        plt.figure(0)
        plt.bar(species_list, species_count, color ='#FFD700', width = 0.4)
        plt.title("Number of each species")
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf,format='png', dpi=400)
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

        # create a plot of the age distribution of all the pets
        age_list_id = [10,12,9,11]
        age_list = ["baby","young","adult","senior"]
        baby = 0
        young = 0
        adult = 0
        senior = 0
        for obj in objects:
            if obj.age.id == 10:
                baby += 1
            elif obj.age.id == 12:
                young += 1
            elif obj.age.id == 9:
                adult += 1
            elif obj.age.id == 11:
                senior += 1
        age_count = [baby, young, adult, senior]

        plt.figure(1)
        plt.bar(age_list, age_count, color ='#FF81C0', width = 0.4)
        plt.title("Age distribution of all species")
        figAge = plt.gcf()
        bufAge = io.BytesIO()
        figAge.savefig(bufAge,format='png', dpi=400)
        bufAge.seek(0)
        stringAge = base64.b64encode(bufAge.read())
        uriAge = urllib.parse.quote(stringAge)

        # create a plot showing the sex/age relation
        sex_list_id = [5,6,7,8]
        age_mean_for_each_group = [0.5, 3, 6.5, 12]

        pet_female_baby, pet_female_young, pet_female_adult, pet_female_senior = population_pyramid(objects, sex_list_id[0], sex_list_id[2])
        pet_male_baby, pet_male_young, pet_male_adult, pet_male_senior = population_pyramid(objects, sex_list_id[1], sex_list_id[3])

        #define x and y limits
        y = range(0, len(age_mean_for_each_group))
        x_male = [pet_male_baby, pet_male_young, pet_male_adult, pet_male_senior]
        x_female = [pet_female_baby, pet_female_young, pet_female_adult, pet_female_senior]

        #define plot parameters
        fig, axes = plt.subplots(ncols=2, sharey=True, figsize=(9, 6))

        #specify background color and plot title
        plt.figure(2)
        plt.figtext(.5,.9,"Population Pyramid ", fontsize=15, ha='center')

        #define male and female bars
        axes[0].barh(y, x_male, align='center', color='royalblue')
        axes[0].set(title='Males')
        axes[1].barh(y, x_female, align='center', color='lightpink')
        axes[1].set(title='Females')

        #adjust grid parameters and specify labels for y-axis
        axes[1].grid()
        axes[0].set(yticks=y, yticklabels=age_mean_for_each_group)
        axes[0].invert_xaxis()
        axes[0].grid()

        figPyramid = plt.gcf()
        bufPyramid = io.BytesIO()
        figPyramid.savefig(bufPyramid,format='png', dpi=400)
        bufPyramid.seek(0)
        stringPyramid = base64.b64encode(bufPyramid.read())
        uriPyramid = urllib.parse.quote(stringPyramid)

        # create scatter plot of breed and color
        breed_color_dict = defaultdict(lambda:"Not Present")
        breed_set = set()
        color_set = set()
        breed_id_set = set()
        color_id_set = set()
        for pet in objects:
            breed_set.add(str(pet.breed))
            color_set.add(str(pet.color))
            breed_id_set.add(pet.breed.id)
            color_id_set.add(pet.color.id)
            if  breed_color_dict[(pet.breed.id, pet.color.id)] != "Not Present":
                breed_color_dict[(pet.breed.id, pet.color.id)].append(1)
            else:
                breed_color_dict[(pet.breed.id, pet.color.id)] = [1]

        x_breed = []
        y_color = []
        for breed, color in breed_color_dict.keys():
            x_breed.append(breed)
            y_color.append(color)

        cmaps = np.random.rand(len(x_breed))
        dict_value = np.array([len(value) for value in breed_color_dict.values()])
        area_value = dict_value * 0.1
        area = (100 * area_value)**2  # 0 to 15 point radii

        plt.figure(4, figsize=(12,9))
        plt.scatter(x_breed, y_color, s=area, c=cmaps, alpha=0.6)
        id_ticks = list(breed_id_set)
        name_ticks = list(breed_set)
        color_id_ticks = list(color_id_set)
        color_name_ticks = list(color_set)
        plt.xticks(id_ticks,name_ticks,rotation=15)
        plt.yticks(color_id_ticks,color_name_ticks,rotation=65)
        figScat = plt.gcf()
        bufScat = io.BytesIO()
        figScat.savefig(bufScat,format='png', dpi=400)
        bufScat.seek(0)
        stringScat = base64.b64encode(bufScat.read())
        uriScat = urllib.parse.quote(stringScat)

        # create a pie chart for sex distribution
        sf = 0
        nm = 0
        f = 0
        m = 0
        for obj in objects:
            if obj.sex.id == sex_list_id[0]:
                sf += 1
            elif obj.sex.id == sex_list_id[1]:
                nm += 1
            elif obj.sex.id == sex_list_id[2]:
                f += 1
            elif obj.sex.id == sex_list_id[3]:
                m += 1
        sizes = []
        labels = []
        if sf > 0:
            sizes.append(sf)
            labels.append("Spayed Female")
        if nm > 0:
            sizes.append(nm)
            labels.append("Neutered Male")
        if f > 0:
            sizes.append(f)
            labels.append("Female")
        if m > 0:
            sizes.append(m)
            labels.append("Male")

        explode = (0.1, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        plt.figure(3)
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=tuple(labels), autopct='%1.1f%%',
                startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        figPie = plt.gcf()
        bufPie = io.BytesIO()
        figPie.savefig(bufPie,format='png', dpi=400)
        bufPie.seek(0)
        stringPie = base64.b64encode(bufPie.read())
        uriPie = urllib.parse.quote(stringPie)

        ctx = {'pet_list':objects, 'search':strval, 'data':uri, 'dataAge':uriAge, \
                'dataPyramid':uriPyramid, 'dataScat':uriScat, 'dataPie':uriPie}
        dump_queries()
        return render(request, 'pets/pet_list.html', ctx)


def population_pyramid(objects, sex1, sex2):
    #0~1 years old, mean: 0.5
    pet_sex_baby = 0
    #2~4 years old, mean:3
    pet_sex_young = 0
    #5~8 years old, mean:6.5
    pet_sex_adult = 0
    # 9~15 years old, mean:12
    pet_sex_senior = 0
    for pet in objects:
        if pet.sex.id == sex1 or pet.sex.id == sex2:
            if str(pet.age) == "baby":
                pet_sex_baby += 1
            elif str(pet.age) == "young":
                pet_sex_young += 1
            elif str(pet.age) == "adult":
                pet_sex_adult += 1
            elif str(pet.age) == "senior":
                pet_sex_senior += 1

    return pet_sex_baby, pet_sex_young, pet_sex_adult, pet_sex_senior

# if __name__=="__main__":
#     population_pyramid(5,7)

