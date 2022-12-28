import torch
import crawler

if __name__ == "__main__":
    print(torch.cuda.is_available())
    custom_crawler = crawler.GoogleImageCrawler()
    custom_crawler.search("dark cloud images")
    
    