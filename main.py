from bs4 import BeautifulSoup
import urllib3
import re
from data.pages import pages
import xml.etree.ElementTree as gfg


http = urllib3.PoolManager()
root = gfg.Element("Drugs")


def extractElement(arr):
    if len(arr) == 0:
        return None
    elif len(arr[0]) >= 1:
        return arr[0][0]
    else:
        return "N/A"


def generateDrugXmlElement(
        id,
        form,
        classification,
        activeSubstance,
        pharmacologicalProperties,
        indications,
        contraindications,
        interactions,
        methodsOfAdministration,
        overdose,
        adverseReactions,
        shelfLife,
        storageConditions,
        diagnosis,
        recommendedAnalogues
):

    item = gfg.Element("item")

    idChild = gfg.SubElement(item, "id")
    idChild.text = id

    formChild = gfg.SubElement(item, "form")
    formChild.text = form

    classificationChild = gfg.SubElement(item, "classification")
    classificationChild.text = classification

    activeSubstanceChild = gfg.SubElement(item, "active-substance")
    activeSubstanceChild.text = activeSubstance

    pharmacologicalPropertiesChild = gfg.SubElement(
        item, "pharmacological-properties")
    pharmacologicalPropertiesChild.text = pharmacologicalProperties

    indicationsChild = gfg.SubElement(item, "indication")
    indicationsChild.text = indications

    contraindicationsChild = gfg.SubElement(item, "contraindications")
    contraindicationsChild.text = contraindications

    interactionsChild = gfg.SubElement(item, "interactions")
    interactionsChild.text = interactions

    methodsOfAdministrationChild = gfg.SubElement(
        item, "methods-of-administration")
    methodsOfAdministrationChild.text = methodsOfAdministration

    overdoseChild = gfg.SubElement(item, "overdose")
    overdoseChild.text = overdose

    adverseReactionsChild = gfg.SubElement(item, "adverse-reactions")
    adverseReactionsChild.text = adverseReactions

    shelfLifeChild = gfg.SubElement(item, "shelf-life")
    shelfLifeChild.text = shelfLife

    storageConditionsChild = gfg.SubElement(item, "storage-conditions")
    storageConditionsChild.text = storageConditions

    diagnosisChild = gfg.SubElement(item, "diagnosis")
    for diagnose in diagnosis:
        diagnoseChild = gfg.SubElement(diagnosisChild, "diagnose")
        diagnoseChild.text = diagnose

    recommendedAnaloguesChild = gfg.SubElement(item, "recommended-analogues")
    for analogue in recommendedAnalogues:
        analogueChild = gfg.SubElement(recommendedAnaloguesChild, "analogue")
        analogueChild.text = analogue

    return item


for page in pages:
    url = http.request('GET', page)
    soup = BeautifulSoup(url.data, "html.parser")
    headerLinks = soup.find(
        "ul", {"itemtype": "http://www.schema.org/SiteNavigationElement"})
    if headerLinks:
        headerLinks.decompose()
    content = soup.find("div", {"class": "content"}).getText()

    # ID
    id = soup.find("div", {"class": "regdata"}).get_text().split(" ")
    if len(id) > 1:
        id = id[1]
    else:
        id = "N/A"

    # Name
    name = soup.article.header.h1.string
    # Form
    form = re.findall(
        "(Лікарська форма[\s\S]{2,}?)Фармакотерапевтична", content),
    form = extractElement(form)
    # Classification
    classification = re.findall("Код.*", content),
    classification = extractElement(classification)
    # Active_substance
    active_substance = re.findall("діюча речовина.*", content),
    active_substance = extractElement(active_substance)
    # Pharmacological_properties
    pharmacological_properties = re.findall(
        "(Фармакологічні властивості[\s\S]{2,}?)Клінічні характеристики", content),
    pharmacological_properties = extractElement(pharmacological_properties)
    # Indications
    indications = re.findall(
        "(Показання[\s\S]{2,}?)Протипоказання", content),
    indications = extractElement(indications)
    # Contraindications
    contraindications = re.findall(
        "(Протипоказання[\s\S]{2,}?)Взаємодія з іншими лікарськими засобами", content),
    contraindications = extractElement(contraindications)
    # Interactions
    interactions = re.findall(
        "(Взаємодія з іншими лікарськими[\s\S]{2,}?)Особливості застосування", content),
    interactions = extractElement(interactions)
    # Method_of_administration
    method_of_administration = re.findall(
        "(Спосіб застосування та дози[\s\S]{2,}?)Діти", content),
    method_of_administration = extractElement(method_of_administration)
    # Overdose
    overdose = re.findall(
        "(Передозування[\s\S]{2,}?)Побічні реакції", content),
    overdose = extractElement(overdose)
    # Adverse_reactions
    adverse_reactions = re.findall(
        "(Побічні реакції[\s\S]{2,}?)Термін придатності", content),
    adverse_reactions = extractElement(adverse_reactions)
    # Shelf_life
    shelf_life = re.findall(
        "(Термін придатності[\s\S]{2,}?)Умови зберігання", content),
    shelf_life = extractElement(shelf_life)
    # Storage_conditions
    storage_conditions = re.findall(
        "(Умови зберігання[\s\S]{2,}?)Упаковка", content),
    storage_conditions = extractElement(storage_conditions)
    # Diagnosis
    diagnosisList = soup.find_all(
        "td", {"class": "text-danger text-nowrap text-right"})
    diagnosis = []
    if len(diagnosisList):
        for diagnose in diagnosisList:
            diagnosis.append(
                re.sub('\r?\n|\t', '', diagnose.getText()))
    # Recommended_analogues
    analoguesList = soup.findAll(
        "div", {"class": "list-group-item"})
    recommended_analogues = []

    if analoguesList:
        for analogue in analoguesList:
            recommended_analogues.append(analogue.div.find(
                "div", {"class": "mb-2 font-weight-bold"}).a.getText())

    root.append
    (
        generateDrugXmlElement
        (
            id,
            form,
            classification,
            active_substance,
            pharmacological_properties,
            indications,
            contraindications,
            interactions,
            method_of_administration,
            overdose,
            adverse_reactions,
            shelf_life,
            storage_conditions,
            diagnosis,
            recommended_analogues
        )
    )


tree = gfg.ElementTree(root)

with open("DrugsOutput.xml", "wb") as output_file:
    tree.write(output_file, encoding='utf-8')