from django.views.generic import ListView
from .models import Voter
from django.db.models import Q

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if v20state:
            queryset = queryset.filter(v20state=(v20state == 'on'))
        if v21town:
            queryset = queryset.filter(v21town=(v21town == 'on'))
        if v21primary:
            queryset = queryset.filter(v21primary=(v21primary == 'on'))
        if v22general:
            queryset = queryset.filter(v22general=(v22general == 'on'))
        if v23town:
            queryset = queryset.filter(v23town=(v23town == 'on'))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['score_range'] = range(6)
        return context


from django.views.generic import DetailView

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'


from django.views.generic import ListView
from .models import Voter
import plotly.express as px
import plotly.io as pio

class VoterGraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = super().get_queryset()
        party = self.request.GET.get('party')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v22general = self.request.GET.get('v22general')
        v23town = self.request.GET.get('v23town')

        if party:
            queryset = queryset.filter(party_affiliation=party)
        if min_dob:
            queryset = queryset.filter(date_of_birth__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__lte=max_dob)
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)
        if v20state:
            queryset = queryset.filter(v20state=(v20state == 'on'))
        if v21town:
            queryset = queryset.filter(v21town=(v21town == 'on'))
        if v21primary:
            queryset = queryset.filter(v21primary=(v21primary == 'on'))
        if v22general:
            queryset = queryset.filter(v22general=(v22general == 'on'))
        if v23town:
            queryset = queryset.filter(v23town=(v23town == 'on'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        birth_years = voters.values_list('date_of_birth', flat=True)
        birth_years = [date.year for date in birth_years if date]
        birth_year_hist = px.histogram(x=birth_years, nbins=30, title="Distribution of Voters by Year of Birth")
        birth_year_hist.update_layout(xaxis_title="Year of Birth", yaxis_title="Count")
        context['birth_year_hist'] = pio.to_html(birth_year_hist, full_html=False)

        from django.db.models import Count

        party_counts = voters.values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_labels = [item['party_affiliation'] for item in party_counts]
        party_values = [item['count'] for item in party_counts]

        party_pie = px.pie(values=party_values, names=party_labels, title="Distribution of Voters by Party Affiliation")
        context['party_pie'] = pio.to_html(party_pie, full_html=False)


        elections = {
            "2020 State Election": voters.filter(v20state=True).count(),
            "2021 Town Election": voters.filter(v21town=True).count(),
            "2021 Primary Election": voters.filter(v21primary=True).count(),
            "2022 General Election": voters.filter(v22general=True).count(),
            "2023 Town Election": voters.filter(v23town=True).count(),
        }
        election_hist = px.bar(x=list(elections.keys()), y=list(elections.values()), title="Distribution of Voter Participation in Elections")
        election_hist.update_layout(xaxis_title="Election", yaxis_title="Count")
        context['election_hist'] = pio.to_html(election_hist, full_html=False)

        context['score_range'] = range(6)
        return context
