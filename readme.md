## PyErowid

Unofficial api for [Erowid](http://erowid.org/)

If you plan on scrapping the website please read [How to Spider Erowid](https://erowid.org/general/about/about_archives1.shtml#howtospider)

## install

    pip install pyerowid

    
## usage

         from pyerowid import Erowid
        
        # getting substances - chemicals, pharms, herbs, animals, plants, smarts
        
        chemicals = Erowid.get_chemicals()
        print chemicals[0].keys()
        names = [c["name"] for c in chemicals]
        print names
        
        """
        ['url', 'other_names', 'name', 'effects']
        [u'absinthe', u'acetylfentanyl', u'adrenochrome', u'aet', u'alcohol', u'alpha-pvp', u'amitriptyline', u'amphetamine', u'amt', u'ayahuasca', u'barbiturates', u'bk-mbdb', u'bromo-dragonfly', u'bufotenin', u'bz', u'bzp', u'caffeine', u'cannabinoids', u'capsaicin', u'carbogen', u'cathinone', u'chloroform', u'chocolate', u'cocaine / crack', u'desomorphine', u'det', u'dipt', u'dmt', u'dob', u'doc', u'doi', u'dom', u'dpt', u'dxm', u'ephedrine', u'ether', u'ethylcathinone', u'ethylene', u'ethylphenidate', u'ghb', u'ghv', u'harmala', u'heroin', u'hypocretin', u'iap', u'ibogaine', u'inhalants', u'ketamine', u'lsa', u'lsd', u'lsz', u'maois', u'mbdb', u'mcpp', u'mda', u'mde', u'mdai', u'mdma', u'mdpr', u'mdpv', u'mescaline', u'met', u'methadone', u'methamphetamines', u'methaqualone', u'methiopropamine', u'methoxetamine', u'methoxphenidine', u'methylone', u'mipt', u'mptp', u'nbome', u'nicotine', u'nitrous', u'opiates', u'opium', u'petroleum ether', u'piperazines', u'pcp', u'pma', u'pmma', u'psilocybin & psilocin', u'salvinorin b ethoxymethyl ether', u'scopolamine', u'"spice" product', u'ssris', u'tfmpp', u'thc', u'tma-2', u'toad venom', u'1,4-butanediol', u'2-aminoindan', u'2c-b', u'2c-b-fly', u'2c-c', u'2c-c-nbome', u'2c-d', u'2c-e', u'2c-i', u'2c-i-nbome', u'2c-p', u'2c-t-2', u'2c-t-4', u'2c-t-7', u'2c-t-21', u'3c-p', u'3-meo-pcp', u'4-acetoxy-det', u'4-acetoxy-dipt', u'4-acetoxy-dmt', u'4-acetoxy-mipt', u'4-fluoroamphetamine', u'4-fluoromethcathinone', u'4-hydroxy-dipt', u'4-hydroxy-met', u'4-hydroxy-mipt', u'4-hydroxy-mpt', u'4-meo-pcp', u'4-methylaminorex', u'4-methylmethcathinone', u'4-methylethcathinone', u'4-mta', u'5-it', u'5-meo-amt', u'5-meo-dalt', u'5-meo-dmt', u'5-meo-dipt', u'5-meo-mipt', u'6-apb', u'other chemicals']
        
        """
        
        # parsing a substance page
        
        chem_data = Erowid.parse_page("https://erowid.org/chemicals/lsd/lsd.shtml")
        for key in chem_data:
            print key, ":", chem_data[key]
        
        """
        info : {'basics': 'https://erowid.org/chemicals/lsd/lsd_basics.shtml', 'dose': 'https://erowid.org/chemicals/lsd/lsd_dose.shtml', 'health': 'https://erowid.org/chemicals/lsd/lsd_health.shtml', 'effects': 'https://erowid.org/chemicals/lsd/lsd_effects.shtml', 'images': 'https://erowid.org/chemicals/lsd/lsd_images.shtml', 'law': 'https://erowid.org/chemicals/lsd/lsd_law.shtml', 'chemistry': 'https://erowid.org/chemicals/lsd/lsd_chemistry.shtml'}
        picture : https://erowid.org/chemicals/lsd/images/lsd_summary1.jpg
        name : lsd-25
        url : https://erowid.org/chemicals/lsd/
        other_names : [u'acid', u'l', u'tabs', u'blotter', u'doses', u'trips']
        effects : Psychedelic
        chem_name : d-lysergic acid diethylamide
        description : LSD is the best known and most researched psychedelic.  It is the standard against which all other psychedelics are compared.  It is active at extremely low doses and is most commonly available on blotter or in liquid form.
        
        """
        
        # handling experience reports
        
        trip_report = Erowid.random_experience()
        print trip_report.keys()
        
        """ ['url', 'gender', 'age', 'experience', 'drug', 'year', 'date', 'exp_id', 'dosage'] """
        
        trip_report = Erowid.get_experience(1)
        for key in trip_report:
            print key, ":", trip_report[key]
        
        """
        url : https://erowid.org/experiences/exp.php?ID=1
        gender : not specified
        age : not given
         15 minutes after this scary ordeal i begin to settle down, i layed down inside his warm house on the rug, touching and rubbing my hands like everywhere, everything was orgasmic feeling. I took a look at my eyes, i look like satan! it was so cool! Then after about and hour laying on the floor, other people come to his house who i dont even really know, but i just conversed with them with no feeling of stupidity, embarresment or consequences, very cool, i loved it, an hour later my eyes still were dialated but effects were over, it was fantastic
        drug : ecstasy
        year : 2000
        date : may 30, 2000
        exp_id : 1
        dosage : [{'substance': u'mdma', 'form': u'(pill / tablet)', 'method': u'oral', 'ammount': u'0.5 tablets', 'time': u't+ 0:00'}, {'substance': u'mdma', 'form': u'(pill / tablet)', 'method': u'oral', 'ammount': u'0.5 tablets', 'time': u't+ 0:45'}]
        
        """
        
        reports = Erowid.search_reports("1P-LSD")
        print reports[0].keys()
        for report in reports[:5]:
            print report["substance"], report["url"], report["date"]
        
        """
        ['date', 'url', 'substance', 'name', 'author']
        1P-ETH-LAD https://erowid.org/experiences/exp.php?ID=109647 Dec 9 2016
        1P-LSD https://erowid.org/experiences/exp.php?ID=108914 Aug 1 2016
        1P-LSD https://erowid.org/experiences/exp.php?ID=108138 Mar 16 2016
        1P-LSD https://erowid.org/experiences/exp.php?ID=108063 Mar 11 2016
        1P-LSD https://erowid.org/experiences/exp.php?ID=107880 Feb 3 2016
        """        