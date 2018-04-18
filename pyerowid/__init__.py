import requests
from bs4 import BeautifulSoup
import random


__author__ = "jarbasAI"


class Erowid(object):

    @staticmethod
    def extract_experience_text(text):
        try:
            begin_delimiter = '<!-- Start Body -->'
            begin = text.index(begin_delimiter) + len(begin_delimiter)
            end = text.index('<!-- End Body -->')
            return text[begin:end].strip().replace("<BR>", "\n").replace("<br>", "\n").replace("\n\n", " ")
        except ValueError:
            return ''

    @staticmethod
    def _extract_list(base_url):
        response = requests.get(base_url).text
        soup = BeautifulSoup(response, "lxml")
        table = soup.find('table', {'class': 'topic-chart-surround'})
        categories = table.find_all("tr", {'class': 'topic-surround'})[1:]
        fields = []
        for cat in categories:
            chem_data = {}
            name = cat.find("td", {'class': 'topic-name'})
            chem_data["url"] = base_url + name.find("a")["href"]
            chem_data["name"] = name.getText().strip().lower()
            chem_data["other_names"] = cat.find("td", {'class': 'topic-common'}).getText().strip().lower()
            chem_data["effects"] = cat.find("td", {'class': 'topic-desc'}).getText().strip().lower()
            fields.append(chem_data)
        return fields

    @staticmethod
    def get_experience(exp_id):
        base_url = 'https://erowid.org/experiences/exp.php'
        url = base_url+"?ID="+str(exp_id)
        data = {"exp_id": exp_id, "url": url}
        try:

            response = requests.get(url).text
            experience = Erowid.extract_experience_text(response)

            soup = BeautifulSoup(response, "lxml")
            drug = soup.find('div', {'class': 'substance'}).getText().strip().lower().replace("/", ", ")
            experience_data = soup.find('table', {'class': 'footdata'}).getText().strip().lower().split("\n")
            data["drug"] = drug
            data["experience"] = experience
            data["year"] = experience_data[0].split("expid:")[0].replace("exp year: ", "").strip()
            data["gender"] = experience_data[1].replace("gender: ", "").strip()
            data["age"] = experience_data[2].replace("age at time of experience: ", "").strip()
            data["date"] = experience_data[3].replace("published: ", "").split("views:")[0].strip()
            data["dosage"] = []

            dosage_table = soup.find('table', {'class': 'dosechart'})
            ts = dosage_table.find_all("td", {'align': 'right'})
            ammount = dosage_table.find_all("td", {'class': 'dosechart-amount'})
            method = dosage_table.find_all("td", {'class': 'dosechart-method'})
            substance= dosage_table.find_all("td", {'class': 'dosechart-substance'})
            form = dosage_table.find_all("td", {'class': 'dosechart-form'})
            for i in range(len(ts)):
                dosage_data = {}
                dosage_data["time"] = ts[i].getText().lower().replace("dose:", "").strip()
                dosage_data["ammount"] = ammount[i].getText().strip().lower()
                dosage_data["method"] = method[i].getText().strip().lower()
                dosage_data["substance"] = substance[i].getText().strip().lower()
                dosage_data["form"] = form[i].getText().strip().lower()
                data["dosage"].append(dosage_data)
        except Exception as e:
            return None
        return data

    @staticmethod
    def get_categories():
        base_url = 'https://erowid.org/experiences/exp_list.shtml'
        response = requests.get(base_url).text
        categories = []
        for sub in response.split("<!-- Start ")[1:]:
            sub = sub[:sub.find(" -->")]
            categories.append(sub)
        return categories

    @staticmethod
    def get_chemicals():
        base_url = 'https://erowid.org/chemicals/'
        return Erowid._extract_list(base_url)

    @staticmethod
    def get_plants():
        base_url = 'https://erowid.org/plants/'
        return Erowid._extract_list(base_url)

    @staticmethod
    def get_herbs():
        base_url = 'https://erowid.org/herbs/'
        return Erowid._extract_list(base_url)

    @staticmethod
    def get_smarts():
        base_url = 'https://erowid.org/smarts/'
        return Erowid._extract_list(base_url)

    @staticmethod
    def get_animals():
        base_url = 'https://erowid.org/animals/'
        return Erowid._extract_list(base_url)

    @staticmethod
    def parse_page(url):
        base_url = url
        if ".shtml" in base_url:
            base_url = "/".join(base_url.split("/")[:-1]) + "/"
        data = {"url": base_url}
        response = requests.get(url).text
        soup = BeautifulSoup(response, "lxml")
        data["name"] = soup.find('div', {'class': 'title-section'}).getText().strip().lower()
        picture = soup.find('div', {'class': "summary-card-topic-image"}).find("img")
        if picture:
            picture = base_url + picture["src"]
        else:
            picture = ""
        data["picture"] = picture
        data["other_names"] = [n.strip().lower() for n in soup.find('div', {'class': 'sum-common-name'}).getText().split(";")]
        data["description"] = soup.find('div', {'class': "sum-description"}).getText()
        info = soup.find('div', {'class': "summary-card-icon-surround"}).find_all("a")
        urls = {}
        for i in info:
            url = base_url + i["href"]
            name = i.find("img")["alt"].strip().lower()
            urls[name] = url
        data["info"] = urls
        if "/chem" in url or "/pharms" in url or "/smarts" in url:
            data["chem_name"] = soup.find('div', {'class': "sum-chem-name"}).getText()
            data["effects"] = soup.find('div', {'class': "sum-effects"}).getText()
        elif "/animals" in url or "/plants" in url:
            animal_data = soup.find_all('div', {'class': "fgs-row"})
            data["family"] = animal_data[0].find('div', {'class': "family"}).getText()
            data["genus"] = animal_data[1].find('div', {'class': "genus"}).getText()
            data["species"] = animal_data[2].find('div', {'class': "species"}).getText()
            data["effects"] = soup.find('div', {'class': "sum-effects"}).getText()
        elif "/herbs" in url:
            animal_data = soup.find_all('div', {'class': "fgs-row"})
            data["family"] = animal_data[0].find('div', {'class': "family"}).getText()
            data["genus"] = animal_data[1].find('div', {'class': "genus"}).getText()
            data["species"] = animal_data[2].find('div', {'class': "species"}).getText()
            data["uses"] = soup.find('div', {'class': "sum-uses"}).getText()

        return data

    @staticmethod
    def random_experience():
        exp = None
        while exp is None:
            exp = Erowid.get_experience(random.randint(1, 111451))
        return exp

    @staticmethod
    def search_reports(search_term, order="substance"):
        base_url = "https://erowid.org/experiences/"
        search_term = search_term.replace(" ", "+")
        url = base_url + "exp.cgi?Str=" + search_term
        if order == "substance":
            url += "&OldSort=SA"
        elif order in ["date", "recent"]:
            url += "&OldSort=PDD"
        elif order in ["old", "older", "oldest"]:
            url += "&OldSort=PDA"
        elif order in ["rating"]:
            url += "&OldSort=RA"
        elif order is not None:
            url += "&OldSort=" + order

        response = requests.get(url).text
        soup = BeautifulSoup(response, "lxml")
        table = soup.find('table', {'class': "exp-list-table"})
        table = table.find_all("tr", {'class': ""})[2:]
        reports = []
        for r in table:
            report = {}
            fields = r.find_all("td")[1:]
            report["name"] = fields[0].getText()
            report["author"] = fields[1].getText()
            report["substance"] = fields[2].getText()
            report["date"] = fields[3].getText()
            report["url"] = base_url + r.find("a")["href"]
            reports.append(report)
        return reports


reports = Erowid.search_reports("1P-LSD")
print reports[0].keys()
for report in reports[:5]:
    print report["substance"], report["url"], report["date"]