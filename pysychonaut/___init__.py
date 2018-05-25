import requests
from bs4 import BeautifulSoup
import random
import json


__author__ = "jarbasAI"


class Erowid(object):
    drug_slang = {
        'marijuana': "thc", 'hashish': "thc", 'hash': "thc", 'weed': "thc",
        'marijjuana': "thc", 'cannabis': "thc", 'benzo fury': '6-apb', 'l': 'lsd',
        'x': 'mdma', 'speed': 'amphetamine', 'pepper oil': 'capsaicin', 'cpp': 'piperazines',
        'blow': 'cocaine', 'foxy': '5-meo-dipt', 'symmetry': 'salvinorin b ethoxymethyl ether',
        'nexus': '2c-b', 'tea': 'caffeine', 'robo': 'dxm', ' tussin': 'dxm',
        'methylethyltryptamine': 'met', 'it-290': 'amt', 'jwh-018': 'cannabinoids',
        'coffee': 'caffeine', 'mpa': 'methiopropamine', 'ergine': 'lsa',
        'harmine': 'harmala', 'mxe': 'methoxetamine',
        '4-ho-met; metocin; methylcybin': '4-hydroxy-met', 'mdea': 'mde',
        'elavil': 'amitriptyline', 'bk-mdma': 'methylone', 'eve': 'mde',
        'a2': 'piperazines', 'dimitri': 'dmt', 'plant food': 'mdpv', 'dr. bob': 'dob', 'doctor bob': 'dob',
        'mini thins': 'ephedrine', 'meth': 'methamphetamines', 'acid': 'lsd',
        'etc.': 'nbome', ' wine': 'alcohol', 'toad venom': 'bufotenin', ' methyl-j': 'mbdb',
        'krokodil': 'desomorphine', ' 5-hydroxy-dmt': 'bufotenin', ' 3-cpp': 'mcpp',
        'special k': 'ketamine', 'ice': 'methamphetamines',
        'nrg-1': 'mdpv', ' gravel': 'alpha-pvp', 'whippits': 'nitrous', 'g': 'ghb',
        'k': 'ketamine', ' harmaline': 'harmala', 'bob': 'dob', '4-ace': '4-acetoxy-dipt',
        'quaaludes': 'methaqualone', ' opium': 'opiates', 'u4ea': '4-methylaminorex',
        'meopp': 'piperazines', 'methcathinone': 'cathinone', 'horse': 'heroin',
        'haoma': 'harmala', 'unknown': '"spice" product', '4-b': '1,4-butanediol',
        'naptha': 'petroleum ether', 'beer': 'alcohol', 'bees': '2c-b',
        '2c-bromo-fly': '2c-b-fly', 'flatliner': '4-mta', 'orexins': 'hypocretin',
        "meduna's mixture": 'carbogen', 'bdo': '1,4-butanediol',
        'fatal meperedine-analog contaminant': 'mptp', 'piperazine': 'bzp', '4-ma': 'pma',
        'paramethoxyamphetamine': 'pma', 'eden': 'mbdb', 'theobromine': 'chocolate',
        'la-111': 'lsa', 'lysergamide': 'lsa', 'yaba': 'methamphetamines',
        'ethyl cat': 'ethylcathinone', 'stp': 'dom', '2c-c-nbome': 'nbome',
        'morphine': 'opiates', 'flakka': 'alpha-pvp', 'yage': 'ayahuasca',
        'ecstasy': 'mdma', 'ludes': 'methaqualone', 'golden eagle': '4-mta',
        '4-mma': 'pmma', 'o-dms': '5-meo-amt', 'liquor': 'alcohol',
        'mephedrone': '4-methylmethcathinone', '1': '1,4-butanediol', 'phencyclidine': 'pcp',
        'crystal': 'methamphetamines', 'pink adrenaline': 'adrenochrome',
        '4-mec': '4-methylethcathinone', 'green fairy': 'absinthe', 'laa': 'lsa',
        'cp 47': 'cannabinoids', 'paramethoxymethylamphetamine': 'pmma',
        '5-meo': '5-meo-dmt', 'alpha': '5-meo-amt', 'mescaline-nbome': 'nbome',
        '25c-nbome': '2c-c-nbome', 'flephedrone': '4-fluoromethcathinone',
        'bzp': 'piperazines', 'codeine': 'opiates', 'foxy methoxy': '5-meo-dipt',
        '25i-nbome': '2c-i-nbome', '3c-bromo-dragonfly': 'bromo-dragonfly', 'mdai': 'mdai',
        'tfmpp': 'piperazines'
    }

    @staticmethod
    def extract_experience_text(text):
        try:
            begin_delimiter = '<!-- Start Body -->'
            begin = text.index(begin_delimiter) + len(begin_delimiter)
            end = text.index('<!-- End Body -->')
            return text[begin:end].strip().replace("<BR>", "\n").replace("<br>", "\n").replace("\n\n", " ").replace("<br/>", "\n")
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
            name = soup.find('div', {'class': 'title'}).getText().strip()
            author = soup.find('div', {'class': 'author'}).getText().strip()
            drug = soup.find('div', {'class': 'substance'}).getText().strip().lower().replace("/", ", ")
            experience_data = soup.find('table', {'class': 'footdata'}).getText().strip().lower().split("\n")
            data["name"] = name
            data["author"] = author
            data["substance"] = drug
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
    def get_pharms():
        base_url = 'https://erowid.org/pharms/'
        return Erowid._extract_list(base_url)

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
            report["exp_id"] = report["url"].split("=")[1]
            reports.append(report)
        return reports


class PsychonautWiki(object):
    drug_slang = {
        'marijuana': "thc", 'hashish': "thc", 'hash': "thc", 'weed': "thc",
        'marijjuana': "thc", 'cannabis': "thc", 'benzo fury': '6-apb', 'l': 'lsd',
        'x': 'mdma', 'speed': 'amphetamine', 'pepper oil': 'capsaicin', 'cpp': 'piperazines',
        'blow': 'cocaine', 'foxy': '5-meo-dipt', 'symmetry': 'salvinorin b ethoxymethyl ether',
        'nexus': '2c-b', 'tea': 'caffeine', 'robo': 'dxm', ' tussin': 'dxm',
        'methylethyltryptamine': 'met', 'it-290': 'amt', 'jwh-018': 'cannabinoids',
        'coffee': 'caffeine', 'mpa': 'methiopropamine', 'ergine': 'lsa',
        'harmine': 'harmala', 'mxe': 'methoxetamine',
        '4-ho-met; metocin; methylcybin': '4-hydroxy-met', 'mdea': 'mde',
        'elavil': 'amitriptyline', 'bk-mdma': 'methylone', 'eve': 'mde',
        'a2': 'piperazines', 'dimitri': 'dmt', 'plant food': 'mdpv', 'dr. bob': 'dob', 'doctor bob': 'dob',
        'mini thins': 'ephedrine', 'meth': 'methamphetamines', 'acid': 'lsd',
        'etc.': 'nbome', ' wine': 'alcohol', 'toad venom': 'bufotenin', ' methyl-j': 'mbdb',
        'krokodil': 'desomorphine', ' 5-hydroxy-dmt': 'bufotenin', ' 3-cpp': 'mcpp',
        'special k': 'ketamine', 'ice': 'methamphetamines',
        'nrg-1': 'mdpv', ' gravel': 'alpha-pvp', 'whippits': 'nitrous', 'g': 'ghb',
        'k': 'ketamine', ' harmaline': 'harmala', 'bob': 'dob', '4-ace': '4-acetoxy-dipt',
        'quaaludes': 'methaqualone', ' opium': 'opiates', 'u4ea': '4-methylaminorex',
        'meopp': 'piperazines', 'methcathinone': 'cathinone', 'horse': 'heroin',
        'haoma': 'harmala', 'unknown': '"spice" product', '4-b': '1,4-butanediol',
        'naptha': 'petroleum ether', 'beer': 'alcohol', 'bees': '2c-b',
        '2c-bromo-fly': '2c-b-fly', 'flatliner': '4-mta', 'orexins': 'hypocretin',
        "meduna's mixture": 'carbogen', 'bdo': '1,4-butanediol',
        'fatal meperedine-analog contaminant': 'mptp', 'piperazine': 'bzp', '4-ma': 'pma',
        'paramethoxyamphetamine': 'pma', 'eden': 'mbdb', 'theobromine': 'chocolate',
        'la-111': 'lsa', 'lysergamide': 'lsa', 'yaba': 'methamphetamines',
        'ethyl cat': 'ethylcathinone', 'stp': 'dom', '2c-c-nbome': 'nbome',
        'morphine': 'opiates', 'flakka': 'alpha-pvp', 'yage': 'ayahuasca',
        'ecstasy': 'mdma', 'ludes': 'methaqualone', 'golden eagle': '4-mta',
        '4-mma': 'pmma', 'o-dms': '5-meo-amt', 'liquor': 'alcohol',
        'mephedrone': '4-methylmethcathinone', '1': '1,4-butanediol', 'phencyclidine': 'pcp',
        'crystal': 'methamphetamines', 'pink adrenaline': 'adrenochrome',
        '4-mec': '4-methylethcathinone', 'green fairy': 'absinthe', 'laa': 'lsa',
        'cp 47': 'cannabinoids', 'paramethoxymethylamphetamine': 'pmma',
        '5-meo': '5-meo-dmt', 'alpha': '5-meo-amt', 'mescaline-nbome': 'nbome',
        '25c-nbome': '2c-c-nbome', 'flephedrone': '4-fluoromethcathinone',
        'bzp': 'piperazines', 'codeine': 'opiates', 'foxy methoxy': '5-meo-dipt',
        '25i-nbome': '2c-i-nbome', '3c-bromo-dragonfly': 'bromo-dragonfly', 'mdai': 'mdai',
        'tfmpp': 'piperazines'}

    def __init__(self):
        self.substance_list = self.get_substance_list()
        self.substances = self.get_substance_data()

    def extract_substance_name(self, sentence):

        words = sentence.lower().split(" ")
        found = False
        # check for drug slang names
        for substance in self.drug_slang:
            substance = substance.lower()
            name = self.drug_slang[substance].strip()
            for idx, word in enumerate(words):
                if substance == word:
                    found = name
                    break

        # check substance list
        for substance in self.substance_list:
            substance = substance.lower()
            for idx, word in enumerate(words):
                if substance == word:
                    found = substance
                    break

        if found:
            # match case, psychonaut wiki doesn't like lower-case
            subs = self.substance_list
            substances = [s.lower() for s in subs]
            substance = found.lower()
            if substance in substances:
                found = subs[substances.index(substance)]

        return found

    def search_psychonaut_wiki(self, substance):
        s = self.extract_substance_name(substance)
        if not s:
            print("Warning, this query does not seem to contain a valid substance name")
        else:
            substance = s

        url = "https://api.psychonautwiki.org/?query=%7B%0A%20%20%20%20substances(query%3A%20%22" + substance + "%22)%20%7B%0A%20%20%20%20%20%20%20%20name%0A%0A%20%20%20%20%20%20%20%20%23%20routes%20of%20administration%0A%20%20%20%20%20%20%20%20roas%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20name%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20dose%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20units%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20threshold%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20heavy%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20common%20%7B%20min%20max%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20light%20%7B%20min%20max%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20strong%20%7B%20min%20max%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20duration%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20afterglow%20%7B%20min%20max%20units%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20comeup%20%7B%20min%20max%20units%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20duration%20%7B%20min%20max%20units%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20offset%20%7B%20min%20max%20units%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20onset%20%7B%20min%20max%20units%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20peak%20%7B%20min%20max%20units%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20total%20%7B%20min%20max%20units%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20bioavailability%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20min%20max%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%0A%20%20%20%20%20%20%20%20%23%20subjective%20effects%0A%20%20%20%20%20%20%20%20effects%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20name%20url%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%7D"
        return json.loads(requests.get(url).text)["data"]

    @staticmethod
    def get_substance_list():
        base_url = "https://psychonautwiki.org/wiki/Summary_index"
        response = requests.get(base_url).text
        soup = BeautifulSoup(response, "lxml")

        table = soup.findAll('div', {'class': 'panel radius'})
        substances = []
        for panel in table:
            subs = panel.find_all("li", {"class": "featured list-item"})
            for s in subs:
                subcat = s.find("span", {"class": "mw-headline"})
                i = 0
                if subcat is not None:
                    subcat = subcat.getText()
                s = s.find_all("a")
                if subcat is not None and s[0].getText() == subcat:
                    i = 1
                for substance in s[i:]:
                    sub_name = substance.getText().replace("/Summary", "").replace("(page does not exist)", "").strip()
                    substances.append(sub_name)
        return substances

    @staticmethod
    def get_substance_data():
        base_url = "https://psychonautwiki.org/wiki/Summary_index"
        response = requests.get(base_url).text
        soup = BeautifulSoup(response, "lxml")

        table = soup.findAll('div', {'class': 'panel radius'})
        substances = {}
        for panel in table:
            categorie = panel.find('span', {'class': 'mw-headline'})
            name = categorie["id"]
            try:
                url = "https://psychonautwiki.org/" + categorie.find("a")["href"]
            except:
                url = None
            if name not in substances:
                substances[name] = {"url": url}

            subs = panel.find_all("li", {"class": "featured list-item"})
            for s in subs:
                subcat = s.find("span", {"class": "mw-headline"})
                i = 0
                if subcat is not None:
                    subcat = subcat.getText()
                    substances[name][subcat] = {}
                s = s.find_all("a")
                if subcat is not None and s[0].getText() == subcat:
                    try:
                        url = "https://psychonautwiki.org/" + s[0]["href"]
                    except:
                        url = None
                    i = 1
                    substances[name][subcat]["url"] = url
                for substance in s[i:]:
                    sub_name = substance.getText().replace("/Summary", "").replace("(page does not exist)", "").strip()
                    if subcat:
                        substances[name][subcat][sub_name] = "https://psychonautwiki.org/" + substance["href"]
                    else:
                        substances[name][sub_name] = "https://psychonautwiki.org/" + substance["href"]
        return substances


class AskTheCaterpillar(object):
    drug_slang = {
            'marijuana': "thc", 'hashish': "thc", 'hash': "thc", 'weed': "thc",
            'marijjuana': "thc", 'cannabis': "thc", 'benzo fury': '6-apb', 'l': 'lsd',
            'x': 'mdma', 'speed': 'amphetamine', 'pepper oil': 'capsaicin', 'cpp': 'piperazines',
            'blow': 'cocaine', 'foxy': '5-meo-dipt', 'symmetry': 'salvinorin b ethoxymethyl ether',
            'nexus': '2c-b', 'tea': 'caffeine', 'robo': 'dxm', ' tussin': 'dxm',
            'methylethyltryptamine': 'met', 'it-290': 'amt', 'jwh-018': 'cannabinoids',
            'coffee': 'caffeine', 'mpa': 'methiopropamine', 'ergine': 'lsa',
            'harmine': 'harmala', 'mxe': 'methoxetamine',
            '4-ho-met; metocin; methylcybin': '4-hydroxy-met', 'mdea': 'mde',
            'elavil': 'amitriptyline', 'bk-mdma': 'methylone', 'eve': 'mde',
            'a2': 'piperazines', 'dimitri': 'dmt', 'plant food': 'mdpv', 'dr. bob': 'dob',
            'doctor bob': 'dob',
            'mini thins': 'ephedrine', 'meth': 'methamphetamines', 'acid': 'lsd',
            'etc.': 'nbome', ' wine': 'alcohol', 'toad venom': 'bufotenin', ' methyl-j': 'mbdb',
            'krokodil': 'desomorphine', ' 5-hydroxy-dmt': 'bufotenin', ' 3-cpp': 'mcpp',
            'special k': 'ketamine', 'ice': 'methamphetamines',
            'nrg-1': 'mdpv', ' gravel': 'alpha-pvp', 'whippits': 'nitrous', 'g': 'ghb',
            'k': 'ketamine', ' harmaline': 'harmala', 'bob': 'dob', '4-ace': '4-acetoxy-dipt',
            'quaaludes': 'methaqualone', ' opium': 'opiates', 'u4ea': '4-methylaminorex',
            'meopp': 'piperazines', 'methcathinone': 'cathinone', 'horse': 'heroin',
            'haoma': 'harmala', 'unknown': '"spice" product', '4-b': '1,4-butanediol',
            'naptha': 'petroleum ether', 'beer': 'alcohol', 'bees': '2c-b',
            '2c-bromo-fly': '2c-b-fly', 'flatliner': '4-mta', 'orexins': 'hypocretin',
            "meduna's mixture": 'carbogen', 'bdo': '1,4-butanediol',
            'fatal meperedine-analog contaminant': 'mptp', 'piperazine': 'bzp', '4-ma': 'pma',
            'paramethoxyamphetamine': 'pma', 'eden': 'mbdb', 'theobromine': 'chocolate',
            'la-111': 'lsa', 'lysergamide': 'lsa', 'yaba': 'methamphetamines',
            'ethyl cat': 'ethylcathinone', 'stp': 'dom', '2c-c-nbome': 'nbome',
            'morphine': 'opiates', 'flakka': 'alpha-pvp', 'yage': 'ayahuasca',
            'ecstasy': 'mdma', 'ludes': 'methaqualone', 'golden eagle': '4-mta',
            '4-mma': 'pmma', 'o-dms': '5-meo-amt', 'liquor': 'alcohol',
            'mephedrone': '4-methylmethcathinone', '1': '1,4-butanediol', 'phencyclidine': 'pcp',
            'crystal': 'methamphetamines', 'pink adrenaline': 'adrenochrome',
            '4-mec': '4-methylethcathinone', 'green fairy': 'absinthe', 'laa': 'lsa',
            'cp 47': 'cannabinoids', 'paramethoxymethylamphetamine': 'pmma',
            '5-meo': '5-meo-dmt', 'alpha': '5-meo-amt', 'mescaline-nbome': 'nbome',
            '25c-nbome': '2c-c-nbome', 'flephedrone': '4-fluoromethcathinone',
            'bzp': 'piperazines', 'codeine': 'opiates', 'foxy methoxy': '5-meo-dipt',
            '25i-nbome': '2c-i-nbome', '3c-bromo-dragonfly': 'bromo-dragonfly', 'mdai': 'mdai',
            'tfmpp': 'piperazines'}

    def __init__(self):
        self.substance_list = PsychonautWiki.get_substance_list()

    def fix_substance_names(self, sentence):

        words = sentence.lower().split(" ")
        found = False
        # check for drug slang names
        for substance in self.drug_slang:
            substance = substance.lower()
            name = self.drug_slang[substance].strip()
            for idx, word in enumerate(words):
                if substance == word:
                    words[idx] = name
                    found = True

        # check substance list
        for substance in self.substance_list:
            substance = substance.lower()
            for idx, word in enumerate(words):
                if substance == word:
                    words[idx] = substance
                    found = True

        if found:
            return " ".join(words)
        # probably not talking about drugs
        return found

    @staticmethod
    def ask_the_caterpillar(query):
        data = requests.post('https://www.askthecaterpillar.com/query', {"query": query})
        data = json.loads(data.text)
        return data["data"]["messages"][0]["content"]
