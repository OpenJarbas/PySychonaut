import requests
from bs4 import BeautifulSoup
import random
import json


__author__ = "jarbasAI"


class Erowid(object):
    drug_slang = {
        u'marijuana': u"thc", u'hashish': u"thc", u'hash': u"thc", u'weed': u"thc",
        u'marijjuana': u"thc", u'cannabis': u"thc", u'benzo fury': u'6-apb', u'l': u'lsd',
        u'x': u'mdma', u'speed': u'amphetamine', u'pepper oil': u'capsaicin', u'cpp': u'piperazines',
        u'blow': u'cocaine', u'foxy': u'5-meo-dipt', u'symmetry': u'salvinorin b ethoxymethyl ether',
        u'nexus': u'2c-b', u'tea': u'caffeine', u'robo': u'dxm', u' tussin': u'dxm',
        u'methylethyltryptamine': u'met', u'it-290': u'amt', u'jwh-018': u'cannabinoids',
        u'coffee': u'caffeine', u'mpa': u'methiopropamine', u'ergine': u'lsa',
        u'harmine': u'harmala', u'mxe': u'methoxetamine',
        u'4-ho-met; metocin; methylcybin': u'4-hydroxy-met', u'mdea': u'mde',
        u'elavil': u'amitriptyline', u'bk-mdma': u'methylone', u'eve': u'mde',
        u'a2': u'piperazines', u'dimitri': u'dmt', u'plant food': u'mdpv', u'dr. bob': u'dob', u'doctor bob': u'dob',
        u'mini thins': u'ephedrine', u'meth': u'methamphetamines', u'acid': u'lsd',
        u'etc.': u'nbome', u' wine': u'alcohol', u'toad venom': u'bufotenin', u' methyl-j': u'mbdb',
        u'krokodil': u'desomorphine', u' 5-hydroxy-dmt': u'bufotenin', u' 3-cpp': u'mcpp',
        u'special k': u'ketamine', u'ice': u'methamphetamines',
        u'nrg-1': u'mdpv', u' gravel': u'alpha-pvp', u'whippits': u'nitrous', u'g': u'ghb',
        u'k': u'ketamine', u' harmaline': u'harmala', u'bob': u'dob', u'4-ace': u'4-acetoxy-dipt',
        u'quaaludes': u'methaqualone', u' opium': u'opiates', u'u4ea': u'4-methylaminorex',
        u'meopp': u'piperazines', u'methcathinone': u'cathinone', u'horse': u'heroin',
        u'haoma': u'harmala', u'unknown': u'"spice" product', u'4-b': u'1,4-butanediol',
        u'naptha': u'petroleum ether', u'beer': u'alcohol', u'bees': u'2c-b',
        u'2c-bromo-fly': u'2c-b-fly', u'flatliner': u'4-mta', u'orexins': u'hypocretin',
        u"meduna's mixture": u'carbogen', u'bdo': u'1,4-butanediol',
        u'fatal meperedine-analog contaminant': u'mptp', u'piperazine': u'bzp', u'4-ma': u'pma',
        u'paramethoxyamphetamine': u'pma', u'eden': u'mbdb', u'theobromine': u'chocolate',
        u'la-111': u'lsa', u'lysergamide': u'lsa', u'yaba': u'methamphetamines',
        u'ethyl cat': u'ethylcathinone', u'stp': u'dom', u'2c-c-nbome': u'nbome',
        u'morphine': u'opiates', u'flakka': u'alpha-pvp', u'yage': u'ayahuasca',
        u'ecstasy': u'mdma', u'ludes': u'methaqualone', u'golden eagle': u'4-mta',
        u'4-mma': u'pmma', u'o-dms': u'5-meo-amt', u'liquor': u'alcohol',
        u'mephedrone': u'4-methylmethcathinone', u'1': u'1,4-butanediol', u'phencyclidine': u'pcp',
        u'crystal': u'methamphetamines', u'pink adrenaline': u'adrenochrome',
        u'4-mec': u'4-methylethcathinone', u'green fairy': u'absinthe', u'laa': u'lsa',
        u'cp 47': u'cannabinoids', u'paramethoxymethylamphetamine': u'pmma',
        u'5-meo': u'5-meo-dmt', u'alpha': u'5-meo-amt', u'mescaline-nbome': u'nbome',
        u'25c-nbome': u'2c-c-nbome', u'flephedrone': u'4-fluoromethcathinone',
        u'bzp': u'piperazines', u'codeine': u'opiates', u'foxy methoxy': u'5-meo-dipt',
        u'25i-nbome': u'2c-i-nbome', u'3c-bromo-dragonfly': u'bromo-dragonfly', u'mdai': u'mdai',
        u'tfmpp': u'piperazines'
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
        u'marijuana': u"thc", u'hashish': u"thc", u'hash': u"thc", u'weed': u"thc",
        u'marijjuana': u"thc", u'cannabis': u"thc", u'benzo fury': u'6-apb', u'l': u'lsd',
        u'x': u'mdma', u'speed': u'amphetamine', u'pepper oil': u'capsaicin', u'cpp': u'piperazines',
        u'blow': u'cocaine', u'foxy': u'5-meo-dipt', u'symmetry': u'salvinorin b ethoxymethyl ether',
        u'nexus': u'2c-b', u'tea': u'caffeine', u'robo': u'dxm', u' tussin': u'dxm',
        u'methylethyltryptamine': u'met', u'it-290': u'amt', u'jwh-018': u'cannabinoids',
        u'coffee': u'caffeine', u'mpa': u'methiopropamine', u'ergine': u'lsa',
        u'harmine': u'harmala', u'mxe': u'methoxetamine',
        u'4-ho-met; metocin; methylcybin': u'4-hydroxy-met', u'mdea': u'mde',
        u'elavil': u'amitriptyline', u'bk-mdma': u'methylone', u'eve': u'mde',
        u'a2': u'piperazines', u'dimitri': u'dmt', u'plant food': u'mdpv', u'dr. bob': u'dob', u'doctor bob': u'dob',
        u'mini thins': u'ephedrine', u'meth': u'methamphetamines', u'acid': u'lsd',
        u'etc.': u'nbome', u' wine': u'alcohol', u'toad venom': u'bufotenin', u' methyl-j': u'mbdb',
        u'krokodil': u'desomorphine', u' 5-hydroxy-dmt': u'bufotenin', u' 3-cpp': u'mcpp',
        u'special k': u'ketamine', u'ice': u'methamphetamines',
        u'nrg-1': u'mdpv', u' gravel': u'alpha-pvp', u'whippits': u'nitrous', u'g': u'ghb',
        u'k': u'ketamine', u' harmaline': u'harmala', u'bob': u'dob', u'4-ace': u'4-acetoxy-dipt',
        u'quaaludes': u'methaqualone', u' opium': u'opiates', u'u4ea': u'4-methylaminorex',
        u'meopp': u'piperazines', u'methcathinone': u'cathinone', u'horse': u'heroin',
        u'haoma': u'harmala', u'unknown': u'"spice" product', u'4-b': u'1,4-butanediol',
        u'naptha': u'petroleum ether', u'beer': u'alcohol', u'bees': u'2c-b',
        u'2c-bromo-fly': u'2c-b-fly', u'flatliner': u'4-mta', u'orexins': u'hypocretin',
        u"meduna's mixture": u'carbogen', u'bdo': u'1,4-butanediol',
        u'fatal meperedine-analog contaminant': u'mptp', u'piperazine': u'bzp', u'4-ma': u'pma',
        u'paramethoxyamphetamine': u'pma', u'eden': u'mbdb', u'theobromine': u'chocolate',
        u'la-111': u'lsa', u'lysergamide': u'lsa', u'yaba': u'methamphetamines',
        u'ethyl cat': u'ethylcathinone', u'stp': u'dom', u'2c-c-nbome': u'nbome',
        u'morphine': u'opiates', u'flakka': u'alpha-pvp', u'yage': u'ayahuasca',
        u'ecstasy': u'mdma', u'ludes': u'methaqualone', u'golden eagle': u'4-mta',
        u'4-mma': u'pmma', u'o-dms': u'5-meo-amt', u'liquor': u'alcohol',
        u'mephedrone': u'4-methylmethcathinone', u'1': u'1,4-butanediol', u'phencyclidine': u'pcp',
        u'crystal': u'methamphetamines', u'pink adrenaline': u'adrenochrome',
        u'4-mec': u'4-methylethcathinone', u'green fairy': u'absinthe', u'laa': u'lsa',
        u'cp 47': u'cannabinoids', u'paramethoxymethylamphetamine': u'pmma',
        u'5-meo': u'5-meo-dmt', u'alpha': u'5-meo-amt', u'mescaline-nbome': u'nbome',
        u'25c-nbome': u'2c-c-nbome', u'flephedrone': u'4-fluoromethcathinone',
        u'bzp': u'piperazines', u'codeine': u'opiates', u'foxy methoxy': u'5-meo-dipt',
        u'25i-nbome': u'2c-i-nbome', u'3c-bromo-dragonfly': u'bromo-dragonfly', u'mdai': u'mdai',
        u'tfmpp': u'piperazines'}

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
            print "Warning, this query does not seem to contain a valid substance name"
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
            u'marijuana': u"thc", u'hashish': u"thc", u'hash': u"thc", u'weed': u"thc",
            u'marijjuana': u"thc", u'cannabis': u"thc", u'benzo fury': u'6-apb', u'l': u'lsd',
            u'x': u'mdma', u'speed': u'amphetamine', u'pepper oil': u'capsaicin', u'cpp': u'piperazines',
            u'blow': u'cocaine', u'foxy': u'5-meo-dipt', u'symmetry': u'salvinorin b ethoxymethyl ether',
            u'nexus': u'2c-b', u'tea': u'caffeine', u'robo': u'dxm', u' tussin': u'dxm',
            u'methylethyltryptamine': u'met', u'it-290': u'amt', u'jwh-018': u'cannabinoids',
            u'coffee': u'caffeine', u'mpa': u'methiopropamine', u'ergine': u'lsa',
            u'harmine': u'harmala', u'mxe': u'methoxetamine',
            u'4-ho-met; metocin; methylcybin': u'4-hydroxy-met', u'mdea': u'mde',
            u'elavil': u'amitriptyline', u'bk-mdma': u'methylone', u'eve': u'mde',
            u'a2': u'piperazines', u'dimitri': u'dmt', u'plant food': u'mdpv', u'dr. bob': u'dob',
            u'doctor bob': u'dob',
            u'mini thins': u'ephedrine', u'meth': u'methamphetamines', u'acid': u'lsd',
            u'etc.': u'nbome', u' wine': u'alcohol', u'toad venom': u'bufotenin', u' methyl-j': u'mbdb',
            u'krokodil': u'desomorphine', u' 5-hydroxy-dmt': u'bufotenin', u' 3-cpp': u'mcpp',
            u'special k': u'ketamine', u'ice': u'methamphetamines',
            u'nrg-1': u'mdpv', u' gravel': u'alpha-pvp', u'whippits': u'nitrous', u'g': u'ghb',
            u'k': u'ketamine', u' harmaline': u'harmala', u'bob': u'dob', u'4-ace': u'4-acetoxy-dipt',
            u'quaaludes': u'methaqualone', u' opium': u'opiates', u'u4ea': u'4-methylaminorex',
            u'meopp': u'piperazines', u'methcathinone': u'cathinone', u'horse': u'heroin',
            u'haoma': u'harmala', u'unknown': u'"spice" product', u'4-b': u'1,4-butanediol',
            u'naptha': u'petroleum ether', u'beer': u'alcohol', u'bees': u'2c-b',
            u'2c-bromo-fly': u'2c-b-fly', u'flatliner': u'4-mta', u'orexins': u'hypocretin',
            u"meduna's mixture": u'carbogen', u'bdo': u'1,4-butanediol',
            u'fatal meperedine-analog contaminant': u'mptp', u'piperazine': u'bzp', u'4-ma': u'pma',
            u'paramethoxyamphetamine': u'pma', u'eden': u'mbdb', u'theobromine': u'chocolate',
            u'la-111': u'lsa', u'lysergamide': u'lsa', u'yaba': u'methamphetamines',
            u'ethyl cat': u'ethylcathinone', u'stp': u'dom', u'2c-c-nbome': u'nbome',
            u'morphine': u'opiates', u'flakka': u'alpha-pvp', u'yage': u'ayahuasca',
            u'ecstasy': u'mdma', u'ludes': u'methaqualone', u'golden eagle': u'4-mta',
            u'4-mma': u'pmma', u'o-dms': u'5-meo-amt', u'liquor': u'alcohol',
            u'mephedrone': u'4-methylmethcathinone', u'1': u'1,4-butanediol', u'phencyclidine': u'pcp',
            u'crystal': u'methamphetamines', u'pink adrenaline': u'adrenochrome',
            u'4-mec': u'4-methylethcathinone', u'green fairy': u'absinthe', u'laa': u'lsa',
            u'cp 47': u'cannabinoids', u'paramethoxymethylamphetamine': u'pmma',
            u'5-meo': u'5-meo-dmt', u'alpha': u'5-meo-amt', u'mescaline-nbome': u'nbome',
            u'25c-nbome': u'2c-c-nbome', u'flephedrone': u'4-fluoromethcathinone',
            u'bzp': u'piperazines', u'codeine': u'opiates', u'foxy methoxy': u'5-meo-dipt',
            u'25i-nbome': u'2c-i-nbome', u'3c-bromo-dragonfly': u'bromo-dragonfly', u'mdai': u'mdai',
            u'tfmpp': u'piperazines'}

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
