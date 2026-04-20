#!/usr/bin/env python3
"""Generate branded PDF content calendar for CEEFM Kft."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas

# Brand colors
NAVY = HexColor("#0F1A2E")
GOLD = HexColor("#B8860B")
IVORY = HexColor("#F5F0E8")
CHARCOAL = HexColor("#1C2B3A")
WARM_GRAY = HexColor("#6B6560")
SAGE = HexColor("#4A6741")
WHITE = HexColor("#FFFFFF")
LIGHT_GOLD = HexColor("#F0E6D0")

# Page dimensions
PAGE_W, PAGE_H = A4

# Posts data
POSTS = [
    {
        "num": 1, "date": "Tuesday, April 1", "week": 1,
        "type": "Company/Service", "topic": "Introducing CEEFM. 12 years. 200+ projects. Three countries.",
        "en": "Most people never think about facility management. Until something breaks.\n\nCEEFM has spent 12 years making sure it does not.\n\nWe manage cleaning, maintenance, and operations for hotels, apartment buildings, and student housing across Hungary, Romania, and Slovakia. Over 200 projects completed. A 9.5 client satisfaction rating.\n\nWe started in Budapest in 2012. Today we serve properties across Central and Eastern Europe.\n\nOur work is simple: keep buildings running. Keep tenants comfortable. Keep costs predictable.\n\nIf you manage a property in Budapest and want a partner who shows up on time and solves problems before they become emergencies, let's talk.\n\noffice@ceefm.eu | +36 30 600 5400",
        "hu": "A legtobb ember nem gondol a letesitmenykezelesre. Amig valami el nem romlik.\n\nA CEEFM 12 eve azon dolgozik, hogy ez ne tortenjen meg.\n\nTakaritast, karbantartast es uzemeltetest vegzunk szallodak, lakoepuletek es diakszallasok szamara Magyarorszagon, Romaniaban es Szlovakiaban. Tobb mint 200 befejezett projekt. 9,5-os ugyfel-elegedettsegi ertek.\n\n2012-ben Budapesten indultunk. Ma Kozep- es Kelet-Europa szerte szolgalunk ingatlanokat.\n\nA munkank egyszeru: az epuletek mukodjenek. A lakoknak legyen kenyelmes. A koltsegek legyenek kiszamithatoak.\n\nHa Budapesten ingatlant kezel es megbizhato partnert keres, aki idoben erkezik es a problemakat meg azelott megoldja, mielott surgossa valnak, keressen minket.\n\noffice@ceefm.eu | +36 30 600 5400",
        "image": "Wide-angle photo of a clean, well-lit Budapest apartment building lobby or hotel reception area. Morning light. No people needed. Focus on the space looking pristine and welcoming. CEEFM logo watermark in corner.",
        "time": "9:00 AM CEST"
    },
    {
        "num": 2, "date": "Wednesday, April 2", "week": 1,
        "type": "Industry Insight", "topic": "Spring maintenance checklist for Budapest property managers",
        "en": "April in Budapest means one thing for property managers: spring maintenance season.\n\nHere is what should be on your checklist right now:\n\n1. HVAC filter replacement. Winter buildup reduces efficiency by up to 25%.\n2. Roof and gutter inspection. Budapest's freeze-thaw cycles cause damage that shows up in spring.\n3. Window seal checks. Failing seals mean higher cooling costs all summer.\n4. Common area deep clean. Lobbies, stairwells, parking areas. Winter grime accumulates.\n5. Fire safety equipment testing. Extinguishers, alarms, emergency lighting. Compliance is not optional.\n6. Exterior facade review. Cracks from winter expansion need attention before they worsen.\n\nSkip any of these and you pay more later. Every time.\n\nWhat would you add to this list?",
        "hu": "Az aprilis Budapesten a letesitmenykezelok szamara egyet jelent: tavaszi karbantartasi szezon.\n\nEz most legyen a csekklistajan:\n\n1. Klimaberendezes szurocsereje. A teli lerakodas akar 25%-kal is csokkenti a hatekonysagot.\n2. Teto- es ereszcsatorna-ellenorzes. A budapesti fagyas-olvadas ciklusok tavaszra mutatjak meg a karokat.\n3. Ablaktornitesek ellenorzese. A hibas tomitesek egesznyaron magasabb hutesi koltsegeket jelentenek.\n4. Kozos teruletek melytisztitasa. Aulak, lepcsohazak, parkolok. A teli szennyezodes felgyulemlik.\n5. Tuzvedelmi berendezesek tesztelese. Oltokeszulekek, riasztok, veszviilagitas. A megfeleles nem valasztas kerdese.\n6. Kulso homlokzat felulvizsgalata. A teli tagulasos repedeskeket meg a rosszabbodas elott kell kezelni.\n\nHa ezek kozul barmit kihagy, kesobb tobbet fizet. Minden alkalommal.\n\nMit tenne meg hozza a listahoz?",
        "image": "Flat-lay style graphic with maintenance icons: wrench, thermometer, checklist, building outline. Clean design on light background. CEEFM brand colors.",
        "time": "9:00 AM CEST"
    },
    {
        "num": 3, "date": "Thursday, April 3", "week": 1,
        "type": "Team/Culture", "topic": "What 5 AM looks like at a Budapest hotel",
        "en": "5:00 AM. The hotel lobby is quiet.\n\nOur team is already on-site.\n\nBy the time the first guest walks to breakfast, three floors of rooms are already cleaned. Fresh linens. Restocked minibars. Bathrooms that pass a white-glove check.\n\nHotel housekeeping is not glamorous work. It is detailed work. It is invisible when done right. And guests notice immediately when it is not.\n\nOur housekeeping supervisors run shifts for properties across Budapest's city center. They manage schedules, quality checks, and supply chains for cleaning materials.\n\nThe best compliment we receive? \"We did not even notice.\"\n\nThat is exactly the point.",
        "hu": "Reggel 5:00. A szalloda aulaja csendes.\n\nA csapatunk mar a helyszinen van.\n\nMire az elso vendeg elindul reggelizni, harom emelet szobai mar tisztak. Friss agynemuk. Feltoltott minibarok. Feher kesztyu tesztet kiallo furdoszobak.\n\nA szallodai hazvezeteseg nem latvanyo munka. Reszletekre figyelo munka. Lathatatlan, ha jol csinaljak. Es a vendegek azonnal eszreveszik, ha nem.\n\nHazvezetesegi felugyeloink muletokat iranyitanak Budapest belvarosaban. Beosztasokat, minosegi ellenorzeseket es tisztitoszer-ellatasi lancokat kezelnek.\n\nA legjobb boka, amit kapunk? \"Eszre sem vettuk.\"\n\nPontosan ez a lenyeg.",
        "image": "Black-and-white or muted-tone photo of a neatly made hotel bed, shot from a low angle. Crisp sheets, pillows perfectly arranged. Early morning light through window.",
        "time": "8:30 AM CEST"
    },
    {
        "num": 4, "date": "Tuesday, April 8", "week": 2,
        "type": "Company/Service", "topic": "Why CEEFM uses eco-friendly cleaning products",
        "en": "We stopped using conventional cleaning chemicals three years ago.\n\nNot because it was trendy. Because the numbers made sense.\n\nEco-friendly products cost 15-20% more per unit. But they reduce sick days among our cleaning staff by roughly a third. They eliminate chemical damage to surfaces, which cuts replacement costs. And they satisfy the sustainability requirements that more hotel chains now demand from subcontractors.\n\nIn apartment buildings, residents with allergies and small children notice the difference. Property managers get fewer complaints.\n\nOur cleaning team uses biodegradable, EU Ecolabel-certified products across all Budapest properties. Same hygiene standards. Lower long-term cost. Safer for everyone in the building.\n\nGreen cleaning is not a marketing decision. It is an operations decision.",
        "hu": "Harom eve hagytuk abba a hagyomanyos tisztitoszerek hasznalatat.\n\nNem azert, mert trendi volt. Azert, mert a szamok igazoltak.\n\nA kornyezetbarat termekek darabonkent 15-20%-kal tobbe kerulnek. De a takarito szemelyzet tappenzet kozel egyharmadaval csokkentik. Megszuntetik a feluletek kemiai karosodasat, ami csokkenti a cserkoltsegeket. Es teljesitik azokat a fenntarthatosagi kovetelmenyeket, amelyeket egyre tobb szallodaanc elvar az alvallalkozoktol.\n\nLakoepuletekben az allergiasok es a kisgyermekes csaladok erzik a kulonbseget. Az ingatlankezelok kevesebb panaszt kapnak.\n\nTakarito csapatunk bioleborathato, EU okocimkes termekeket hasznal minden budapesti ingatlanon. Ugyanaz a higienes szinvonal. Alacsonyabb hosszu tavu koltseg. Biztonsagosabb mindenki szamara az epuletben.\n\nA zold takaritas nem marketingdontes. Uzemeltetesi dontes.",
        "image": "Close-up of eco-friendly cleaning products with EU Ecolabel visible, arranged on a clean surface. Natural light. A gloved hand reaching for one of the bottles.",
        "time": "9:00 AM CEST"
    },
    {
        "num": 5, "date": "Wednesday, April 9", "week": 2,
        "type": "Industry Insight", "topic": "Energy costs in Budapest buildings and what FM can do about it",
        "en": "Energy costs for Budapest commercial buildings rose 40% between 2022 and 2025.\n\nMost property managers absorbed the increase. Few optimized.\n\nHere is what we see working across our managed properties:\n\nLED lighting retrofits. Payback period: 8-14 months. After that, pure savings.\n\nSmart HVAC scheduling. Matching heating and cooling to actual occupancy instead of fixed schedules cuts energy use by 15-20%.\n\nBuilding envelope audits. Finding and fixing air leaks is the cheapest energy upgrade available. Most buildings have them. Few check.\n\nMotion-sensor lighting in common areas. Stairwells, parking garages, storage rooms. Lights that run 24/7 when nobody is there are burning money.\n\nRegular boiler and chiller maintenance. A 5% efficiency drop from neglected maintenance compounds fast across a full building.\n\nNone of this requires major capital investment. It requires attention.",
        "hu": "A budapesti kereskedelmi epuletek energiakoltsegei 2022 es 2025 kozott 40%-kal novekedtek.\n\nA legtobb ingatlankezelo elviselte a novekedest. Kevesen optimalizaltak.\n\nIme, mit latunk mukodni a kezelt ingatlanainkon:\n\nLED vilagitas-atalakitas. Megteerulesi ido: 8-14 honap. Utana tiszta megtakaritas.\n\nIntelligens HVAC utemezees. A futes es hutes valos kihasznaltsaghoz igazitasa a fix utemezesek helyett 15-20%-kal csokkenti az energiafelhasznalast.\n\nEpuletburkolat-auditok. A legszivargas felkutatasa es javitasa a legolcsobb elerheto energia-korszeerusites.\n\nMozgaserzekelos vilagitas kozos teruleten. A 24 oraban ego lampak, amikor senki sincs ott, penzt egetnek.\n\nRendszeres kazan- es huto karbantartas. Az elhanyagolt karbantartasbol eredo 5%-os hatekonysagcsokkeens egy egesz epuletben gyorsan osszegzodik.\n\nEhhez nem kell nagy tokebefektetes. Odafigyelees kell.",
        "image": "Infographic-style visual showing energy cost reduction percentages. Simple bar chart or icons. Navy and gold color scheme on ivory background.",
        "time": "12:00 PM CEST"
    },
    {
        "num": 6, "date": "Thursday, April 10", "week": 2,
        "type": "Team/Culture", "topic": "What makes a good facility supervisor",
        "en": "We have hired over 50 facility supervisors in 12 years.\n\nThe best ones share three traits:\n\nThey notice what others miss. A flickering light in a stairwell. A door that closes half a second slower than it should. A cleaning pattern that leaves streaks only visible at certain angles.\n\nThey communicate before problems escalate. A good supervisor calls you to say \"the elevator is making a new sound, I have scheduled the technician for Thursday\" before you call them to say \"the elevator is broken.\"\n\nThey respect the people on their team. Cleaning and maintenance staff work early hours, physical shifts, and often thankless roles. A supervisor who treats them well has lower turnover. Lower turnover means consistent quality.\n\nTechnical skills can be trained. These three traits cannot.\n\nIf this sounds like you, we are hiring: office@ceefm.eu",
        "hu": "12 ev alatt tobb mint 50 letesitmenykezelesi felugyelot vettunk fel.\n\nA legjobbak harom kozos vonast mutatnak:\n\nEszreveszik, amit masok nem. Egy villogo lampat a lepcsohazban. Egy ajtot, ami fel masodperccel lassabban csukodik, mint kellene.\n\nKommunikalnak, mielott a problemak sullyosbodnak. Egy jo felugyeloo felhivja ont, hogy \"a lift uj hangot ad ki, csutortokre beideztem a szerelot\" mielott on hivna, hogy \"a lift elromlott.\"\n\nTisztelik a csapatuk tagjait. A takarito es karbantarto szemelyzet koran reggel dolgozik, fizikailag megterheloi muletokban es gyakran halatlan szerepekben.\n\nA technikai keszsegek tanithatoak. Ez a harom tulajdonsag nem.\n\nHa ez onre hasonlit, keresunk munkatarsakat: office@ceefm.eu",
        "image": "Portrait-style photo of a person in professional workwear standing in a building corridor. Confident posture. Real person, not a model.",
        "time": "9:00 AM CEST"
    },
    {
        "num": 7, "date": "Tuesday, April 15", "week": 3,
        "type": "Industry Insight", "topic": "The three hotel housekeeping standards guests actually notice",
        "en": "Hotel guests do not read your housekeeping SOP.\n\nBut they notice three things within 30 seconds of entering a room:\n\nThe bathroom. Specifically: the mirror, the toilet rim, and the drain. If any of those three are not spotless, the entire room feels unclean. Regardless of everything else.\n\nThe smell. Not air freshener. The absence of smell. A room should smell like nothing. Chemical fragrance signals that something is being covered up. Neutral air signals genuine cleanliness.\n\nThe bed. Wrinkle-free sheets and symmetrical pillows. Guests touch the bed first. If the linens feel fresh and the surface is flat and tight, confidence in the room goes up immediately.\n\nEverything else matters too. But these three form the first impression. And first impressions drive reviews.\n\nAt CEEFM, our quality inspections prioritize exactly these checkpoints. Because that is what your guests prioritize.",
        "hu": "A szallodavendegek nem olvassak el a hazvezeteseg muveleti eljarasait.\n\nDe harom dolgot harom masodpercen belul eszrevesznek a szobaba lepes utan:\n\nA furdoszobat. Pontosabban: a tukrot, a WC-peremet es a lefolyot. Ha ezek kozul barmelyik nem makulatlan, az egesz szoba tisztatalannak tunik.\n\nA szagot. Nem legfrissitot. A szag hiannyat. Egy szobanak semmilyen szagunak nem kellene lennie.\n\nAz agyat. Rancmentes lepedok es szimmetrikus parnok. A vendegek eloszor az agyat erintik meg.\n\nMinden mas is szamit. De ez a harom alkotja az elso benyomast. Es az elso benyomas hatarozza meg az ertekeleseket.\n\nA CEEFM-nel a minosegi ellenorzesseink pontosan ezeket az ellenorzo pontokat helyezik eloterbe.",
        "image": "Split image: one half shows a pristine hotel bathroom mirror reflection, the other half shows perfectly made bed linens. Clean, bright photography.",
        "time": "9:00 AM CEST"
    },
    {
        "num": 8, "date": "Wednesday, April 16", "week": 3,
        "type": "Company/Service", "topic": "Student housing FM. Different rules, different challenges.",
        "en": "Student housing is not the same as hotel management. Property managers who treat it the same way lose money.\n\nHere is what is different:\n\nTurnover cycles are fixed. Move-in happens in September. Move-out in June. That two-week window between academic years is your entire deep maintenance window. Miss it and you carry problems for 10 months.\n\nDamage patterns are predictable. Kitchens and bathrooms take the most wear. Common room furniture breaks fastest. The first six weeks of the academic year produce the most maintenance tickets.\n\nCommunication must be direct and digital. Students do not read notice boards. Maintenance request systems need to work on mobile. Response expectations are same-day.\n\nCleaning frequency must be higher in common areas. Study rooms, kitchens, laundry rooms. These spaces serve 50-200 people daily.\n\nCEEFM manages student housing facilities in Budapest and across the region. We know the cycle. We plan around it.",
        "hu": "A diakszallas nem ugyanaz, mint a szallodakezeles. Azok az ingatlankezelok, akik ugyanugy kezelik, penzt veszitenek.\n\nIme, mi mas:\n\nA forgasi ciklusok rogzitettek. Bekoltozes szeptemberben. Kikoltozes juniusban.\n\nA karosodasok kiszamithatoak. A konyhak es furdoszobak kopnak a legjobban.\n\nA kommunikacioanak kozvetlennek es digitalisnak kell lennie. A diakok nem olvasnak hirdetotablat.\n\nA takaritasi gyakorisagnak magasabbnak kell lennie a kozos teruleten.\n\nA CEEFM diakszallasokat kezel Budapesten es a regioban. Ismerjuk a ciklust. Tervezunk kore.",
        "image": "Photo of a modern student housing common area or study room. Clean, functional design. Focus on the well-maintained space.",
        "time": "9:00 AM CEST"
    },
    {
        "num": 9, "date": "Thursday, April 17", "week": 3,
        "type": "Industry Insight", "topic": "Smart building technology. What actually delivers ROI.",
        "en": "Every facility management conference in 2026 talks about smart buildings.\n\nMost of the technology being sold has a payback period longer than the contract term. Here is what actually works for mid-size properties in Budapest:\n\nSmart thermostats with occupancy sensing. Cost: 200-400 EUR per unit. Savings: 10-18% on heating and cooling. Payback: under 2 years.\n\nWater leak sensors. Cost: 50-100 EUR per sensor. A single undetected leak can cause 10,000+ EUR in damage.\n\nDigital maintenance ticketing. Cost: 30-80 EUR per month for a property. Benefit: traceable response times, data on recurring issues, accountability.\n\nIoT-connected lighting in common areas. Cost: moderate. Savings: real but slower payback (3-4 years).\n\nDigital twins and AI-driven predictive maintenance? Promising for large portfolios. Overkill for a 50-unit apartment building.\n\nStart with what pays back fastest. Scale from there.",
        "hu": "Minden 2026-os letesitmenykezelesi konferencia az okos epuletekrol beszel.\n\nAz eladott technologia nagy reszenek megteerulesi ideje hosszabb, mint a szerzodees idotartama.\n\nOkos termosztatokk jelenleterrzekelesssel. Koltseg: 200-400 EUR. Megtakaritas: 10-18%. Megteruules: 2 even belul.\n\nVizszivargas-erzekelok. Koltseg: 50-100 EUR. Egyetlen szivaargas 10 000+ EUR kart okozhat.\n\nDigitalis karbantartasi jegykezelo. Koltseg: havi 30-80 EUR.\n\nIoT-kapcsolt vilagitas kozos teruleten. Koltseg: merseekelt. Megteruules: 3-4 ev.\n\nDigitalis ikrek es MI-vezerelt prediktiv karbantartas? Tulzas egy 50 lakaasos epulethez.\n\nKezdje azzal, ami a leggyorsabban terul meg.",
        "image": "Clean tech-forward graphic. Icons: thermostat, water drop sensor, mobile phone with ticket, lightbulb with wifi symbol. Each paired with its ROI number. Navy/gold/ivory palette.",
        "time": "12:00 PM CEST"
    },
    {
        "num": 10, "date": "Tuesday, April 22", "week": 4,
        "type": "Company/Service", "topic": "Sustainability at CEEFM. What we actually do, not what we say.",
        "en": "\"Sustainability\" is the most overused word in facility management marketing.\n\nHere is what it means in our daily operations:\n\nWe use EU Ecolabel-certified cleaning products at every property. No exceptions.\n\nWe sort and track waste volumes monthly across all managed buildings. Our clients get reports showing exactly how much waste each property generates and where reduction is possible.\n\nWe run quarterly energy audits for properties under long-term contracts. Not because it sounds good. Because our clients save money when we do.\n\nOur maintenance schedules prioritize repair over replacement. A reconditioned door closer lasts another 5 years. A replaced one goes to landfill.\n\nWe train every team member on resource efficiency in their first week. Not a slideshow. Practical, on-site training.\n\nWe are not perfect. No FM company is. But we measure, report, and improve. Every quarter.",
        "hu": "A \"fenntarthatosag\" a leginkabb tulhasznalt szo a letesitmenykezelesi marketingben.\n\nIme, mit jelent a napi muveleteinkben:\n\nEU okocimkes tisztitoszereket hasznalunk minden ingatlanon. Kivetel nelkul.\n\nHavonta valogatjuk es kovetjuk a hulladekmennyisegeket az osszes kezelt epuletben.\n\nNegyedevente energiaauditot vegzunk a hosszu tavu szerzodes alatt allo ingatlanoknal.\n\nKarbantartasi utemterveink a javitast reszesitik elonyben a cserevel szemben.\n\nMinden csapattagot az elso heten kepezunk az eroforras-hatekonysag teren.\n\nNem vagyunk tokeletesek. Egyetlen FM ceg sem az. De merunk, jelentsunk es fejlodunk. Minden negyedevben.",
        "image": "Photo composition showing CEEFM operations: eco cleaning products in use, a waste sorting station, a maintenance worker repairing equipment.",
        "time": "9:00 AM CEST (Earth Day)"
    },
    {
        "num": 11, "date": "Wednesday, April 23", "week": 4,
        "type": "Industry Insight", "topic": "Budapest's property boom and what it means for facility management",
        "en": "Budapest's office market is 4.25 million square meters. Second largest in Central Europe after Warsaw.\n\nThe hotel sector added 1,200+ new rooms in 2025 alone. Student housing developments are expanding across Districts 8, 9, and 13.\n\nMore buildings means more demand for facility management. But not just any facility management.\n\nProperty owners are shifting from \"find the cheapest cleaning company\" to \"find a partner who manages everything under one contract.\" Integrated FM contracts are growing at nearly 7% annually in the CEE region.\n\nWhat is driving this?\n\nComplexity. A modern mixed-use building needs cleaning, HVAC maintenance, security, energy management, waste handling, and tenant communication. Coordinating five separate vendors costs more than one integrated provider. And problems fall through the gaps.\n\nIf you manage property in Budapest, the question is no longer whether you need professional facility management. It is whether your current provider can keep up with what your building actually requires.",
        "hu": "Budapest irodapiaca 4,25 millio negyzetmeter. Kozep-Europa masodik legnagyobb piaca Varso utan.\n\nA szallodai szektor egyedul 2025-ben tobb mint 1200 uj szobaaval bovult.\n\nTobb epulet tobb letesitmenykezelesi igenyt jelent. De nem akarmilyen letesitmenykezelest.\n\nAz ingatlantulajdonosok a \"keressuk a legolcsobb takarito ceget\" megkozelitestol a \"keressunk egy partnert, aki mindent egy szerzodes alatt kezel\" fele mozgnak.\n\nMi hajtja ezt? Az osszetettseg.\n\nHa Budapesten ingatlant kezel, a kerdes mar nem az, hogy szuksege van-e professzionalis letesitmenykezelesre. Hanem az, hogy a jelenlegi szolgaltatoja kepes-e leelepest tartani azzal, amit az epulete valoban igenyel.",
        "image": "Aerial or elevated photo of Budapest skyline showing modern buildings and construction. Or a data-driven visual: simple map of Budapest districts with growth indicators.",
        "time": "9:00 AM CEST"
    },
    {
        "num": 12, "date": "Thursday, April 24", "week": 4,
        "type": "Company/Service", "topic": "Five reasons to outsource facility management",
        "en": "You can manage your building's facilities in-house. Many property owners do.\n\nHere are five reasons they eventually stop:\n\n1. Staff coverage. A sick day or resignation creates an immediate service gap. An FM company has backup staff available within hours. You do not.\n\n2. Procurement costs. We buy cleaning materials, maintenance parts, and equipment at volume pricing. A single building cannot match those rates.\n\n3. Compliance tracking. Fire safety inspections, hygiene certifications, equipment servicing records. An FM company tracks these automatically. In-house teams often let them slip until audit time.\n\n4. Scalability. Adding a second property does not mean doubling your internal team. It means expanding a contract.\n\n5. Focus. Managing cleaners, electricians, plumbers, and security is a full-time job. If that is not your core business, it is consuming time that belongs elsewhere.\n\nOutsourcing is not about cutting corners. It is about putting each task in the hands of people who do it every day.\n\nCEEFM has been that partner for 200+ properties. If your building needs one, reach out: office@ceefm.eu",
        "hu": "Kezelhetik az epuletuk letesitmenyeit haazon belul. Sok ingatlantulajdonos igy tesz.\n\nIme ot ok, amiert vegul abbahagyjak:\n\n1. Szemelyzeti lefedettseeg. Egy betegszabadsag vagy felmonddas azonnali szolgaltatasi rest teremt.\n\n2. Beszerzesi koltsegek. Mi nagybani aeron vasarolunk. Egyetlen epulet nem tudja felvenni ezeket az arakat.\n\n3. Megfelelosegi nyomon kovetes. Egy FM ceg automatikusan koveti ezeket.\n\n4. Skalazhatosag. Egy masodik ingatlan hozzaadasa nem jelenti a belso csapat megkeetszerezeset.\n\n5. Fokusz. Takaritok, villanyszerelok, vizvezetek-szerelok kezelese teljes allasu munka.\n\nA kiszervezes nem a sarkok levaagasarol szol. Arrol, hogy minden feladatot olyan emberek kezebe adunk, akik minden nap ezt csinaljaak.\n\nA CEEFM tobb mint 200 ingatlannak volt ilyen partnere. Keressen minket: office@ceefm.eu",
        "image": "Clean comparison graphic: left side 'In-house' with complexity icons, right side 'CEEFM' with a single unified interface. Navy and gold on ivory.",
        "time": "9:00 AM CEST"
    },
]

TYPE_COLORS = {
    "Company/Service": GOLD,
    "Industry Insight": NAVY,
    "Team/Culture": SAGE,
}


def draw_cover_background(c, doc):
    """Draw cover page background."""
    w, h = A4
    # Full ivory background
    c.setFillColor(IVORY)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    # Navy header band (top 35%)
    band_h = h * 0.35
    c.setFillColor(NAVY)
    c.rect(0, h - band_h, w, band_h, fill=1, stroke=0)
    # Gold left accent bar
    c.setFillColor(GOLD)
    c.rect(0, 0, 6, h, fill=1, stroke=0)
    # Gold rule below header band
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(6, h - band_h, w, h - band_h)


def draw_page_background(c, doc):
    """Draw standard page background."""
    w, h = A4
    c.setFillColor(IVORY)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    # Gold left accent bar
    c.setFillColor(GOLD)
    c.rect(0, 0, 6, h, fill=1, stroke=0)
    # Navy top line
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.5)
    c.line(20, h - 20, w - 20, h - 20)
    # Footer
    c.setFont("Helvetica", 7.5)
    c.setFillColor(WARM_GRAY)
    c.drawCentredString(w / 2, 22, "BridgeWorks  |  office@bridgeworks.agency  |  bridgeworks.agency")


# Styles
style_title = ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=26, textColor=WHITE, leading=32, alignment=TA_LEFT)
style_subtitle = ParagraphStyle("Subtitle", fontName="Helvetica", fontSize=13, textColor=GOLD, leading=18, alignment=TA_LEFT)
style_meta = ParagraphStyle("Meta", fontName="Helvetica", fontSize=10, textColor=WARM_GRAY, leading=14, alignment=TA_LEFT)
style_h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=18, textColor=NAVY, leading=24, spaceBefore=16, spaceAfter=8)
style_h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=13, textColor=NAVY, leading=18, spaceBefore=12, spaceAfter=4)
style_h3 = ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=10, textColor=CHARCOAL, leading=14, spaceBefore=6, spaceAfter=2)
style_body = ParagraphStyle("Body", fontName="Helvetica", fontSize=8.5, textColor=CHARCOAL, leading=12, spaceBefore=2, spaceAfter=2)
style_body_sm = ParagraphStyle("BodySm", fontName="Helvetica", fontSize=7.5, textColor=CHARCOAL, leading=10, spaceBefore=1, spaceAfter=1)
style_label = ParagraphStyle("Label", fontName="Helvetica-Bold", fontSize=8, textColor=GOLD, leading=11)
style_image_brief = ParagraphStyle("ImageBrief", fontName="Helvetica-Oblique", fontSize=7.5, textColor=WARM_GRAY, leading=10, spaceBefore=2, spaceAfter=4)
style_tag = ParagraphStyle("Tag", fontName="Helvetica-Bold", fontSize=7, textColor=WHITE, leading=9, alignment=TA_CENTER)


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=20*mm, rightMargin=15*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )

    story = []

    # ---- COVER PAGE (manual via first page template) ----
    # We use a spacer to push content into the navy band area
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("CEEFM Kft", style_title))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("LinkedIn Content Calendar", style_title))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("April 2026", style_subtitle))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Powered by BridgeWorks", style_subtitle))
    story.append(Spacer(1, 45*mm))

    # Cover metadata
    cover_meta = [
        "<b>Client:</b> CEEFM Kft",
        "<b>Period:</b> April 1-30, 2026",
        "<b>Frequency:</b> 3 posts per week (Tuesday, Wednesday, Thursday)",
        "<b>Total posts:</b> 12",
        "<b>Content mix:</b> 40% company/service | 40% industry insight | 20% team/culture",
        "<b>Posting time:</b> 9:00 AM CEST (Budapest) unless noted otherwise",
        "<b>Voice:</b> CEEFM brand voice. Professional, specific, solution-oriented.",
    ]
    for line in cover_meta:
        story.append(Paragraph(line, style_meta))
        story.append(Spacer(1, 1*mm))

    story.append(PageBreak())

    # ---- OVERVIEW TABLE PAGE ----
    story.append(Paragraph("Content Overview", style_h1))
    story.append(Spacer(1, 3*mm))

    table_data = [["#", "Date", "Day", "Type", "Topic"]]
    for p in POSTS:
        table_data.append([
            str(p["num"]),
            p["date"].split(", ")[1],
            p["date"].split(",")[0],
            p["type"],
            p["topic"][:60] + ("..." if len(p["topic"]) > 60 else "")
        ])

    t = Table(table_data, colWidths=[8*mm, 22*mm, 22*mm, 32*mm, 80*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 7.5),
        ("TEXTCOLOR", (0, 1), (-1, -1), CHARCOAL),
        ("BACKGROUND", (0, 1), (-1, -1), IVORY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [IVORY, LIGHT_GOLD]),
        ("GRID", (0, 0), (-1, -1), 0.5, WARM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 8*mm))

    # Mix breakdown
    story.append(Paragraph("Content Mix", style_h2))
    mix_data = [
        ["Type", "Count", "Percentage"],
        ["Company/Service", "5", "42%"],
        ["Industry Insight", "5", "42%"],
        ["Team/Culture", "2", "16%"],
    ]
    mt = Table(mix_data, colWidths=[50*mm, 25*mm, 25*mm])
    mt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("TEXTCOLOR", (0, 1), (-1, -1), CHARCOAL),
        ("BACKGROUND", (0, 1), (-1, -1), IVORY),
        ("GRID", (0, 0), (-1, -1), 0.5, WARM_GRAY),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(mt)
    story.append(PageBreak())

    # ---- INDIVIDUAL POST PAGES ----
    current_week = 0
    for p in POSTS:
        if p["week"] != current_week:
            current_week = p["week"]
            story.append(Paragraph(f"Week {current_week}", style_h1))
            story.append(Spacer(1, 2*mm))

        # Post header with colored type tag
        type_color = TYPE_COLORS.get(p["type"], NAVY)
        post_header = f'<font color="{NAVY.hexval()}"><b>Post {p["num"]}</b></font> &nbsp; <font color="{type_color.hexval()}">{p["date"]}</font> &nbsp; | &nbsp; <font color="{type_color.hexval()}"><b>{p["type"]}</b></font> &nbsp; | &nbsp; <font color="{WARM_GRAY.hexval()}">{p["time"]}</font>'
        story.append(Paragraph(post_header, style_h3))
        story.append(Paragraph(f'<b>{p["topic"]}</b>', style_h2))
        story.append(Spacer(1, 1*mm))

        # English version
        story.append(Paragraph('<font color="#B8860B"><b>ENGLISH</b></font>', style_label))
        for para in p["en"].split("\n\n"):
            para = para.replace("\n", "<br/>")
            story.append(Paragraph(para, style_body_sm))

        story.append(Spacer(1, 3*mm))

        # Hungarian version
        story.append(Paragraph('<font color="#B8860B"><b>MAGYAR</b></font>', style_label))
        for para in p["hu"].split("\n\n"):
            para = para.replace("\n", "<br/>")
            story.append(Paragraph(para, style_body_sm))

        story.append(Spacer(1, 3*mm))

        # Image brief
        story.append(Paragraph('<font color="#B8860B"><b>IMAGE BRIEF</b></font>', style_label))
        story.append(Paragraph(p["image"], style_image_brief))

        # Separator
        story.append(Spacer(1, 4*mm))
        if p["num"] % 2 == 0 and p["num"] < 12:
            story.append(PageBreak())
        elif p["num"] < 12:
            # Light divider line between posts on same page
            pass

    # ---- NOTES PAGE ----
    story.append(PageBreak())
    story.append(Paragraph("Notes", style_h1))
    notes = [
        "All times are CEST (Central European Summer Time, UTC+2).",
        "Hungarian translations written without diacritics for maximum platform compatibility. If CEEFM prefers accented Hungarian, these can be updated.",
        "Image briefs are designed for either original photography or graphic design. Canva templates recommended.",
        "Posts 5 and 9 are scheduled at 12:00 PM for lunchtime engagement.",
        "Post 10 aligns with Earth Day (April 22) for organic reach boost.",
        "Each post ends with a soft CTA or engagement question where natural.",
    ]
    for n in notes:
        story.append(Paragraph(f"  {n}", style_body))
        story.append(Spacer(1, 2*mm))

    # Build with appropriate page templates
    doc.build(
        story,
        onFirstPage=draw_cover_background,
        onLaterPages=draw_page_background,
    )
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    import sys
    output = sys.argv[1] if len(sys.argv) > 1 else "CEEFM-April-Content-Calendar.pdf"
    build_pdf(output)
