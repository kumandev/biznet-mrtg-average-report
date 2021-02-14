from selenium import webdriver
import time, sys, os
from PIL import Image
from pytesseract import pytesseract 

#set clock, test
clock = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
target_date = sys.argv[1]

path_ss = "screenshot/"+target_date+"/"
path_croped = "croped/"+target_date+"/"
path_log = "log/"

os.system("mkdir "+path_ss.replace("/","\\"))
os.system("mkdir "+path_croped.replace("/","\\"))

log_name = "log-average-"+target_date+".txt"

# initiate web driver
driver = webdriver.Firefox(executable_path=r'C:\webdriver\geckodriver.exe')
#login
driver.get("http://mrtg-branch.biznetnetworks.com/cacti/graph_view.php")
time.sleep(0.5)
driver.find_element_by_xpath("/html/body/form/table/tbody/tr[5]/td[2]/input").send_keys("username")
driver.find_element_by_xpath("/html/body/form/table/tbody/tr[6]/td[2]/input").send_keys("password")
driver.find_element_by_xpath("/html/body/form/table/tbody/tr[8]/td/input").click()


def download_graph(i, start_date, end_date):
	img_ss = target_date+" "+clock[i+1][:2]+".png"

	driver.get("http://mrtg-branch.biznetnetworks.com/cacti/graph_view.php")
	time.sleep(0.5)

	#set start target_date
	driver.find_element_by_xpath("//*[@id=\"date1\"]").clear()
	driver.find_element_by_xpath("//*[@id=\"date1\"]").send_keys(start_date)
	#set end target_date
	driver.find_element_by_xpath("//*[@id=\"date2\"]").clear()
	driver.find_element_by_xpath("//*[@id=\"date2\"]").send_keys(end_date)

	#click refresh
	driver.find_element_by_xpath("/html/body/table/tbody/tr[5]/td/div/table[1]/tbody/tr/td/table/tbody/tr[3]/td/form/table/tbody/tr/td[12]/input[1]").click()
	time.sleep(1)

	#click magnifier for detailed graph
	driver.find_element_by_xpath("/html/body/table/tbody/tr[5]/td/div/table[2]/tbody/tr/td/table/tbody/tr[2]/td[1]/table/tbody/tr/td[2]/a[1]/img").click()
	time.sleep(1)

	#get image src of the graph
	graph_src = driver.find_element_by_xpath("//*[@id=\"zoomGraphImage\"]").get_attribute("src")
	print("["+img_ss+"] "+graph_src)

	#download detailed graph
	driver.get(graph_src)
	time.sleep(0.5)
	driver.save_screenshot(path_ss+img_ss)

def extract_text(i):
	img_ss = path_ss+target_date+" "+clock[i+1][:2]+".png"
	img_crop = path_croped+"crop-"+target_date+clock[i+1][:2]+".png"

	img = Image.open(img_ss)
	# img_crop_data = img.crop((677, 525, 758, 578))
	img_crop_data = img.crop((720, 403, 793, 450))
	img_crop_data.save(img_crop, quality=100)

	print("["+str(i+1)+"] "+"Extracting data from : "+path_croped+img_ss+" to "+log_name)
	pytesseract.tesseract_cmd = r'C:\tesseract-ocr\tesseract.exe'
	text = pytesseract.image_to_string(img_crop)
	text = text.replace(chr(10), ";").replace(".",",")
	print("Data : "+text)

	text_file = open(path_log+log_name, "a+")
	text_file.write(text+"\n")
	text_file.close()

def main():
	counter = 0
	
	for i in range(0,15):
		if counter < 16:
			download_graph(i,target_date+clock[i],target_date+clock[i+1])
			counter+=1
			if counter == 15:
				for x in range(0,15):
					extract_text(x)
		else:
			print("Do nothing...")

if __name__ == '__main__':
	main()