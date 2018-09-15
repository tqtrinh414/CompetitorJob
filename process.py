import pandas as pd
import pickle

class Company:

    def __init__(self, id = None, major = None, country = None, \
                    employee = None, revenue = None):
        self.id = id
        self.country = country
        self.major = major
        self.employee = employee
        self.revenue =  revenue

    def similariry(self, company, threshold_emp = 100, threshold_reven = 2):
        score = 0
        if self.country == company.country:
            score += 2
        if abs(self.employee - company.employee) <= threshold_emp:
            score += 1
        pair = (self.revenue, company.revenue)
        if max(pair) / (min(pair) + 2) <= threshold_reven:
            score += 1
        return score


class Competitor:

    def __init__(self):
        self.companies = {}
        self.majors = {}

    def load_data(self, companies_path, vertical_path, cache = False):
        if cache:
            self.companies =  pickle.load(open(companies_path))
            self.majors = pickle.load(open(vertical_path))
            return
        df_vertical = pd.read_csv(vertical_path)[['id', 'code']]
        fields = ['company_id', 'vertical_ids', 'country_id', 'staff_qty', 'revenue']
        df_companies = pd.read_csv(companies_path)[fields]
        dct_vertical = {}
        for i in range(df_vertical.shape[0]):
            id, code = df_vertical.ix[i, 'id'], df_vertical.ix[i, 'code'][0]
            dct_vertical[id] = code
        for i in range(df_companies.shape[0]):
            comp_id, ver_id, con_id, staff, reven = df_companies.ix[i, 0], \
                df_companies.ix[i, 1], df_companies.ix[i, 2], \
                    df_companies.ix[i, 3], df_companies.ix[i, 4]
            try:
                major_id = dct_vertical[ver_id]
                new_company = Company(comp_id, major_id, con_id, staff, reven)
                self.companies[comp_id] = new_company
                if major_id not in self.majors:
                    self.majors[major_id] = []
                else:
                    self.majors[major_id].append(comp_id)
            except:
                continue
        pickle.dump(self.companies, open(companies_path + '.pkl', 'wb'))
        pickle.dump(self.majors, open(vertical_path + '.pkl', 'wb'))

    def query(self, id, major, country, employee, revenue):
        company = Company(id, major, country, employee, revenue)
        res = {}
        for c in self.majors[major]:
            res[c] = company.similariry(self.companies[c])
        import operator
        sorted_x = sorted(res.items(), key=operator.itemgetter(1), reverse = True)
        return [x[0] for x in sorted_x[0:10]]


def main():

    competitor = Competitor()
    competitor.load_data('new_data.csv.pkl', 'verticals.csv.pkl', cache = True)
    import time
    start = time.time()
    print(competitor.query(13, 'B', 5, 409, 1976543))
    end = time.time()
    print(end - start)

if __name__=="__main__":
    main()
