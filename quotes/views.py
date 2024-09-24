import random
from django.shortcuts import render

quotes = [
    "When something is important enough, you do it even if the odds are not in your favor.",
    "Failure is an option here. If things are not failing, you are not innovating enough.",
    "Some people don’t like change, but you need to embrace change if the alternative is disaster.",
    "Great companies are built on great products.",
    "It’s OK to have your eggs in one basket as long as you control what happens to that basket.",
    "If you get up in the morning and think the future is going to be better, it is a bright day. Otherwise, it’s not.",
    "Brand is just a perception, and perception will match reality over time.",
    "I think that’s the single best piece of advice: constantly think about how you could be doing things better and questioning yourself.",
    "The first step is to establish that something is possible; then probability will occur."
]

images = [
    "https://media-cldnry.s-nbcnews.com/image/upload/t_fit-1000w,f_auto,q_auto:best/rockcms/2024-08/240806-elon-musk-civil-war-kh-b08ba6.jpg",
    "https://www.nmspacemuseum.org/wp-content/uploads/2019/03/Elon_Musk.jpg",
    "https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781982181284/elon-musk-9781982181284_lg.jpg",
    "https://static.independent.co.uk/2024/09/06/16/elon-musk-controls-satellites-starlink.jpg",
    "https://media.wired.com/photos/650399af65d83ff288720473/master/w_2240,c_limit/If-Elon-Musk-Had-Been-a-Happy-Child,-Would-He-Still-Be-Launching-Rockets--Business-Redux-h_16082330.jpg",
    "https://fortune.com/img-assets/wp-content/uploads/2024/09/GettyImages-2171035708_f7c521-e1727121301200.jpg",
    "https://fortune.com/img-assets/wp-content/uploads/2024/09/GettyImages-2158237818-e1725370605815.jpg",
    "https://image.cnbcfm.com/api/v1/image/106434195-1595357993564-elon.jpg",
    "https://www.economist.com/cdn-cgi/image/width=1424,quality=80,format=auto/media-assets/image/20221008_LDP001.jpg",
    "https://ca-times.brightspotcdn.com/dims4/default/17913ba/2147483647/strip/true/crop/3071x2048+0+0/resize/1200x800!/format/webp/quality/75/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2Fec%2F21%2Fc0faf8844835aa6055d3932e6a5a%2Felon-musk-solarcity-lawsuit-30775.jpg"
]

def quote(request):
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    context = {
        'quote': selected_quote,
        'image': selected_image
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    context = {
        'quotes': quotes,
        'images': images
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    context = {
        'person': "Elon Musk",
        'creator': "Minseok Lee"
    }
    return render(request, 'quotes/about.html', context)