import os, sys
import fitz

def main(fname):
    dstdir = os.path.splitext(fname)[0]
    os.makedirs(dstdir, exist_ok=True)
    with fitz.open(fname) as doc:
        for i, page in enumerate(doc):
            for j, img in enumerate(page.getImageList()):
                x = doc.extractImage(img[0])
                name = os.path.join(dstdir, f"{i:04}_{j:02}.{x['ext']}")
                with open(name, "wb") as ofh:
                    ofh.write(x['image'])

if __name__ == "__main__":
    main(sys.argv[1])