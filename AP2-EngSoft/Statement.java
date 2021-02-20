import java.util.Enumeration;

public abstract class Statement {

    abstract String header(Customer aCustomer);

    abstract String figure(Rental each);

    abstract String footer(Customer aCustomer);


    public String value(Customer aCustomer) {
        Enumeration rentals = aCustomer.getRentals();
        String result = header(aCustomer);
        while (rentals.hasMoreElements()) {
            Rental each = (Rental) rentals.nextElement();
            // show figures for each rental
            result += figure(each);
        }
        // add footer lines
        result += footer(aCustomer);
        return result;
    }
}
